// Analysis-only call prototypes from the public gzcom-dll cISCLua interface.
// Run with -readOnly to preserve the previous Ghidra project; exports record the experiment.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.data.*;
import ghidra.program.model.pcode.HighFunctionDBUtil;
import java.nio.file.*;
import java.util.*;
public class InspectAndRepairLua extends GhidraScript {
 private final DataType ptr=PointerDataType.dataType, integer=IntegerDataType.dataType;
 private void override(long site,String name,DataType result,DataType... arguments) throws Exception {
  var sig=new FunctionDefinitionDataType(name);sig.setCallingConvention("__thiscall");sig.setReturnType(result);
  var args=new ParameterDefinition[arguments.length+1];args[0]=new ParameterDefinitionImpl("this",ptr,null);
  for(int i=0;i<arguments.length;i++)args[i+1]=new ParameterDefinitionImpl("arg"+i,arguments[i],null);
  sig.setArguments(args);
  HighFunctionDBUtil.writeOverride(getFunctionAt(toAddr(0x005fc020)),toAddr(site),sig);
  println("CALL_OVERRIDE "+toAddr(site)+" "+sig.getPrototypeString());
 }
 public void run() throws Exception {
  var out=Path.of(getScriptArgs()[0]);Files.createDirectories(out);
  try(var w=Files.newBufferedWriter(out.resolve("failed-function-inspection.txt"))) {
   for(long raw:new long[]{0x005fc020,0x006ed6e0,0x00775cc0,0x0077c660,0x00808080}) {
    var a=toAddr(raw);var f=getFunctionAt(a);w.write("\nFUNCTION "+a+" "+f.getSignature()+" body="+f.getBody()+"\n");
    var refs=getReferencesTo(a);for(var r:refs)w.write("INCOMING "+r+"\n");
    var listing=currentProgram.getListing();var i=listing.getInstructionBefore(a.subtract(32));
    while(i!=null&&i.getAddress().compareTo(a.add(48))<=0){w.write(i.getAddress()+" "+i+" owner="+getFunctionContaining(i.getAddress())+"\n");i=listing.getInstructionAfter(i.getAddress());}
   }
  }
  override(0x005fc03e,"QueryInterface",BooleanDataType.dataType,UnsignedIntegerDataType.dataType,ptr);
  override(0x005fc046,"GetTop",integer);
  override(0x005fc059,"Type",integer,integer);
  override(0x005fc06e,"GetGlobal",VoidDataType.dataType,ptr);
  override(0x005fc07c,"IsNumber",BooleanDataType.dataType,integer);
  override(0x005fc08b,"ToNumber",DoubleDataType.dataType,integer);
  override(0x005fc09d,"Pop",VoidDataType.dataType,integer);
  override(0x005fc0a8,"ToString",ptr,integer);
  override(0x005fc0d4,"PushNumber",VoidDataType.dataType,DoubleDataType.dataType);
  override(0x005fc0df,"PushNil",VoidDataType.dataType);
  override(0x005fc0ec,"Release",UnsignedIntegerDataType.dataType);
  var d=new DecompInterface();
  try {
   d.openProgram(currentProgram);var result=d.decompileFunction(getFunctionAt(toAddr(0x005fc020)),120,monitor);
   if(result.decompileCompleted()&&result.getDecompiledFunction()!=null) {
    Files.writeString(out.resolve("005fc020.c"),"/* Experimental pseudocode with community cISCLua call-site prototypes.\n * See references/gzcom-dll/gzcom-dll/include/cISCLua.h and src/SCLuaUtil.cpp.\n * Original binary and raw exports remain unchanged. */\n"+result.getDecompiledFunction().getC());
    println("LUA_TYPED_DECOMPILE_SUCCESS");
   } else {Files.writeString(out.resolve("005fc020.failed.txt"),result.getErrorMessage());println("LUA_TYPED_DECOMPILE_FAILED "+result.getErrorMessage());}
  } finally {d.dispose();}
 }
}
