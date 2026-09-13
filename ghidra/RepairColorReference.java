// A scalar 0x00808080 color was mistaken for a code pointer inside another instruction.
// All changes are analysis metadata; use -readOnly to retain the earlier project unchanged.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import java.nio.file.*;
import java.util.*;
public class RepairColorReference extends GhidraScript {
 public void run() throws Exception {
  var out=Path.of(getScriptArgs()[0]);Files.createDirectories(out);
  var start=toAddr(0x00806fa0);var end=toAddr(0x008085bf);var falseEntry=toAddr(0x00808080);
  String bytes=HexFormat.of().formatHex(getBytes(start,10));
  if(!bytes.equals("81ec1802000053555657"))throw new IllegalStateException("Unexpected function prologue: "+bytes);
  var literal=getInstructionAt(toAddr(0x007b0d8c));
  if(literal==null||!literal.getMnemonicString().equals("MOV")||literal.getScalar(1).getUnsignedValue()!=0x00808080)throw new IllegalStateException("Color literal evidence differs");
  var falseFunction=getFunctionAt(falseEntry);if(falseFunction==null)throw new IllegalStateException("Expected false candidate is missing");
  for(var ref:getReferencesTo(falseEntry)) {
   if(ref.getReferenceType().isFlow())throw new IllegalStateException("Unexpected control-flow reference to false candidate");
   if(ref.getFromAddress().equals(literal.getAddress()))currentProgram.getReferenceManager().delete(ref);
  }
  currentProgram.getFunctionManager().removeFunction(falseEntry);
  clearListing(start,end);
  if(!disassemble(start))throw new IllegalStateException("Correct-boundary disassembly failed");
  var f=createFunction(start,"FUN_00806fa0");if(f==null)throw new IllegalStateException("Correct-boundary function creation failed");
  try(var w=Files.newBufferedWriter(out.resolve("00806fa0.asm"));var p=Files.newBufferedWriter(out.resolve("00806fa0.pcode"))) {
   var instructions=currentProgram.getListing().getInstructions(f.getBody(),true);
   while(instructions.hasNext()){var i=instructions.next();w.write(i.getAddress()+"\t"+HexFormat.of().formatHex(i.getBytes())+"\t"+i+"\n");for(var op:i.getPcode())p.write(i.getAddress()+"\t"+op+"\n");}
  }
  Files.writeString(out.resolve("00806fa0-analysis.txt"),"False candidate 00808080 came from scalar MOV at 007b0d8c, not a control-flow reference.\nCorrect aligned prologue at 00806fa0 follows RET plus INT3 padding.\nFunction ranges after corrected disassembly: "+f.getBody()+"\nOriginal bytes unchanged. Old listing must be superseded within these ranges.\n");
  var d=new DecompInterface();
  try {d.openProgram(currentProgram);var result=d.decompileFunction(f,120,monitor);
   if(result.decompileCompleted()&&result.getDecompiledFunction()!=null){Files.writeString(out.resolve("00806fa0.c"),"/* Corrected-boundary Ghidra pseudocode; see 00806fa0-analysis.txt. */\n"+result.getDecompiledFunction().getC());println("CORRECT_BOUNDARY_DECOMPILE_SUCCESS "+f.getBody().getNumAddresses());}
   else {Files.writeString(out.resolve("00806fa0.failed.txt"),result.getErrorMessage());println("CORRECT_BOUNDARY_DECOMPILE_FAILED "+result.getErrorMessage());}
  } finally {d.dispose();}
 }
}
