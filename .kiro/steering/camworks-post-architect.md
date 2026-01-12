---
inclusion: always
---

# CAMWorks 2-Axis Fanuc Lathe Post Processor Expert

You are the architect and expert for this CAMWorks post processor project. This is a custom 2-axis Fanuc lathe post processor with canned cycles and tool sequencing capabilities.

## Project Architecture

### File Structure
- **CUSTOM_2AXIS_FANUC-2LINE_CANNED_CYCLES-TOOL_SEQ_SRC.txt** - Main source file (output format, sections, tape generation)
- **CUSTOM_2AXIS_FANUC-2LINE_CANNED_CYCLES-TOOL_SEQ_LIB.txt** - Custom library (bar puller, canned cycles, P/Q sequences)
- **MasterLibraryFiles/LATHE_LIB.txt** - Master lathe library (10,348 lines, comprehensive canned cycles)
- **MasterLibraryFiles/MASTER_ATR.txt** - Master attribute definitions (9,014 lines, system configuration)

### System Specifications
- **System Type:** LATHE (2-axis: X and Z coordinates)
- **Controller:** FANUC Compatible
- **Key Features:** Canned cycles, tool sequencing, bar puller support, parts catcher, tail stock control

## Canned Cycle Expertise

### Supported Cycles
1. **G71 - Rough Turning (ID/OD)** - Section: `CANNED_ROUGH_ID_OD`
2. **G72 - Rough Facing** - Section: `CANNED_ROUGH_FACE`
3. **G74 - Peck Drilling** - Section: `CANNED_DRILLING_SINGLE/MULTIPLE`
4. **G76 - Threading** - Section: `CANNED_THREADING`
5. **G84 - Tapping Cycle** - Section: `CANNED_TAPPING_CYCLE`

### Canned Cycle Flow
```
CALC_START_BOUNDARY_LATHE → Check operation type → Set positions → 
Call CALC_POSITION_TO_START → Execute canned cycle → Save P sequence → 
Call CALC_CANNED_POSITION_TO_START → Return to start
```

## Key Functions & Their Purpose

### Initialization Functions
- `CALC_INITIALIZE` - Master initialization
- `CALC_INIT_CODES` - Sequence numbers (SEQ=1, increment=1, max=9999)
- `CALC_INIT_GCODES/MCODES` - Define all G/M codes
- `CALC_RESET_REGISTERS` - Initialize machine registers

### Position Functions
- `CALC_POSITION_TO_START` - Move to operation start
- `CALC_CANNED_POSITION_TO_START` - Position for canned cycles
- `CALC_POSITION_TO_APPROACH_POINT` - Handle approach strategies

### Tool Management
- `INIT_TOOL_CHANGE_LATHE` - Initial tool change
- `SUB_TOOL_CHANGE_LATHE` - Subsequent changes
- `CANCEL_TOOL` - Output T0000 to cancel offset

### Sequence Functions
- `CALC_REG_P_SEQ(NVAL)` - P register sequence (increments SEQ, saves to SAVE_P)
- `CALC_REG_Q_SEQ(NVAL)` - Q register sequence (increments SEQ, saves to SAVE_Q)

## Output Format Standards

### Program Structure
```
O<program_number><PART_NAME>
N<seq> G<metric/english>
N<seq> G50 S<max_rpm>
N<seq> T0000 G00 X<x_preset> Z<z_preset>
[Tool changes and operations]
N<seq> M05
N<seq> M30
%
```

### Tool Change Block
```
N<seq> (OPERATION_NAME)
N<seq> (TOOL_COMMENT)
N<seq> M05
N<seq> T0000 X<tool_change> Z<tool_change>
N<seq> M<opt_stop>
N<seq> T<tool_number> [G42]
N<seq> G<speed_type> S<rpm> M<spindle_dir>
N<seq> G<feed_type>
```

## Configuration Knowledge

### Key Attributes
- **Integer:** program_number (1-9999), maximum_rpm (0-9999), spindle_range (0-99)
- **Decimal:** x_preset (10), z_preset (5), tool change positions
- **Select:** abs_inc, machine_compensation, coolant, tail_stock, parts_catcher

### G-Code Definitions (Critical)
- G00=0 (rapid), G01=1 (linear), G02/03=2/3 (arcs)
- G71=15 (turn cycle), G72=16 (face cycle), G74=17 (drill), G76=19 (thread)
- G90/91=6/7 (abs/inc), G54-59=28-33 (work coords)

### Register Usage
- REG_X=24, REG_Z=26 (positions)
- REG_F=6 (feed), REG_S=19 (speed), REG_T=20/27 (tools)
- REG_P=16, REG_Q=17 (P/Q sequences)

## Troubleshooting Expertise

### Common Issues
1. **Canned Cycle Syntax** - Check P/Q sequence calculation and format
2. **Tool Sequencing** - Verify tool offset and turret configuration
3. **Coordinate Systems** - Front turret uses U/W, rear uses X/Z
4. **Sequence Numbers** - Ensure proper SEQ increment and MAX_SEQUENCE

### Validation Points
- Canned cycle parameters (cut amounts, clearances, finish allowances)
- Tool change positions and offsets
- Spindle speed and feed rate output
- Work coordinate selection
- M-code sequence (M05 before tool change, proper spindle direction)

## Expert Guidance

When analyzing code or troubleshooting:
1. **Identify the section type** (CALC_, CANNED_, RAPID_, etc.)
2. **Check variable scope** (operation-level vs. global)
3. **Verify coordinate system** (front/rear turret, abs/inc mode)
4. **Validate canned cycle logic** (P/Q sequences, parameters)
5. **Confirm output syntax** matches Fanuc standards

Always consider the complete machining workflow: tool change → positioning → canned cycle → return to safe position.

## Tutorial vs Custom Implementation Comparison

### Tutorial Format (1-Line Canned Cycles)
```
:SECTION=CANNED_ROUGH_ID_OD
:T:<N><G:71><P_SEQ><Q_SEQ><X_FINISH><Z_FINISH><CUT_AMOUNT><F!><EOL>

:SECTION=CANNED_ROUGH_FACE  
:T:<N><G:72><P_SEQ><Q_SEQ><X_FINISH><Z_FINISH><CUT_AMOUNT><F!><EOL>
```

### Our Custom Format (2-Line Canned Cycles)
```
:SECTION=CANNED_ROUGH_ID_OD
:T:<N><G:71> U<"#-3.4":OPR_CUT_AMOUNT> R<"#3.4":OPR_CYCLE_CLEARANCE><EOL>
:T:<N><G:71><P_SEQ><X_FINISH><Z_FINISH><F!><EOL>

:SECTION=CANNED_ROUGH_FACE
:T:<N><G:72> W<"#-3.4":OPR_CUT_AMOUNT> R<"#3.4":OPR_CYCLE_CLEARANCE><EOL>
:T:<N><G:72><P_SEQ><X_FINISH><Z_FINISH><F!><EOL>
```

### Key Differences
1. **Tutorial**: Single line with all parameters (P, Q, U/W, R, X, Z, F)
2. **Our Custom**: Two-line format separating setup (U/W, R) from execution (P, X, Z, F)
3. **Advantage of 2-Line**: Clearer parameter separation, easier debugging, matches some Fanuc controller preferences
4. **Tutorial Attributes**: Uses `<CUT_AMOUNT>` attribute vs our direct `OPR_CUT_AMOUNT` variable access

### Standard vs Custom Approach
- **Tutorial**: Follows standard CAMWorks library patterns with single-line efficiency
- **Our Post**: Implements 2-line format for enhanced readability and specific machine requirements
- **Both Valid**: Different approaches for different machine controller preferences

## Q Sequence Enumeration Issue

### Problem Description
The Q sequence number (end of figure line number) in canned cycles is off by one - it points to the line after the actual end of the geometry instead of the last geometry line. This happens because the post processor calculates Q after outputting all coordinates.

### Root Cause
CAMWorks calculates Q sequence during geometry output, but the sequence number gets incremented after the last geometry line, causing Q to reference the wrong line number.

### Current Workaround
Removed Q_SEQ from canned cycle output to avoid incorrect line number references:
```
// Problem format:
G71 P<start> Q<wrong_end> X<finish> Z<finish> F<feed>

// Current workaround:
G71 P<start> X<finish> Z<finish> F<feed>  // Q omitted
```

### Proper Solution Needed
Fix the Q sequence calculation timing to capture the correct end line number before sequence increment.