;@============================================================================
;@
;@ Student Name: Ya Qi (Jerry) Liu
;@ Student #: 301255583
;@ Student userid (email): liuyal (liuyal@sfu.ca)
;@
;@ Helpers: Craig Scratchley, Zhen Xiao
;@
;@ Resources:  ARMv5 Architecture Reference Manual, Procedure Call Standard for the ARM® Architecture,
;@             ARM ASSEMBLY LANGUAGE - Fundamentals and Techniques - SECOND EDITION 
;@
;@ Name        : fib-full.s
;@ Description : Submission for Assignment 1.
;@============================================================================

.text; 				          @ Store in ROM

Reset_Handler:

.global Reset_Handler; 		  @ The entry point on reset
					 	
main:						 ;@ The main program	

	ldr sp, =#0x40004000	 ;@ Initialize SP just past the end of RAM
	mov r4, #3;			 	  @ Some value
	mov r12, #0;
	
main_loop:	
	ldr r0, =test_n;       	  @ Load value of N into first argument
	ldr r0, [r0, r12];
	;@ldr r0, #100;			  @  Manual Test
	mov r2, r0;
	bl Compare;				  @ Compare input with 0, 1, 2
	bl sub_fib; 			  @ Find Nth value of the Fibonacci sequence
	bl test;
		
stop:						 ;@ At this point, r4 should be 3
	b stop;					  @ All Test Case Finished
Error_ans:
	b Error_ans;			  @ Failed Test Case
	
sub_fib:						   ;@<Store register(s) and LR to stack>
	 stmdb r13!, {r2-r12, lr}; 		@ Store Multiple, Decrement SP before, update
								   ;@<128-bit Fibonacci Algorithm from Lab 3>
	 ldr r2, =var_a;
	 ldr r3, =var_b;
	 
	 push {r0,r1};			  @ Initialize OF_bit for final overflow
	 mov r1, #0;
	 ldr r0, =OF_bit;
	 str r1, [r0, #0];
	 pop {r0,r1};
	 
	 mrs r7, CPSR;
	 subs r0, r0, #2;		  @ Decrement by 2 to calculate nth fib number
	 msr CPSR,r7;
	 
	 mov r4, r0;			  @ Move n into r4
	 mov r1, #508;			  @ High index
     mov r0, #500;			  @ Low index
	 push {r0, r1}; 
	 
	 subs r0,r0,#4;			  @ Add 1 more word;
	 msr CPSR,r7;
	 
initialize_loop:   
	 msr CPSR, r7;            @ Load a 1 into both variables   
	 mov r12, #0;             @ Constant used for initializing the variables
	 str r12, [r2, r1];       @ Set the value of var_a
	 str r12, [r3, r1];       @ Set the value of var_b					
	 mrs r7, CPSR;
	 subs r1, r1, #4;		  @ Decrement to next word
	 cmp r1, r0;			  @ Until the end
	 bne initialize_loop;

	 msr CPSR, r7;
	 pop {r0, r1};			  @ Complete the initialization for var_a and var_b
	 mov r12, #1;             @ Constant used for initializing LSW of variables
	 str r12, [r2, r1];       @ Set the value of var_a to 1		
	 str r12, [r3, r1]; 	  @ Set the value of var_b to 1 
	 
loop:
	 bl add_128;	 	 	  @ Perform add
 	 bcs overflow;	 	 	  @ Detect if variable overflowed by looking at carry, If so, branch to "overflow"
back:	 					 
	 subs r4, r4, #1;		  @ Decrement the loop counter
	 bne loop;	 	 		  @ Reached the desired term
done:
	 ldr r7, =index_msb;
	 str r0, [r7, #0];
	 mov r0, r3;
	 mov r1, r4;
	 b Restore_R;	 	 	  @ Program done! Restore R.
	 
overflow:					 ;@ Initialize new word for overflow
	 mrs r7, CPSR;
	 cmp r0, #-4;			  
	 beq Final_OF;			  @ If at end of memory, brance to Final_OverFlow
	 msr CPSR,r7;
 
	 mov r12, #1;           
	 str r12, [r3, r0];       @ Set the value of var_b	
	 mov r12, #0;  
	 str r12, [r2, r0];       @ Set the value of var_a
	 
	 mrs r7, CPSR;
	 subs r0, r0, #4;		  @ Decrements lower index
	 msr CPSR,r7;
	 
	 b back;
	 
add_128:					 ;@ Subroutine to load two words from the variables into memory
	 push {r1,lr}; 		      @ Start with the least significant word (word 0)	
	 mrs r7, CPSR;		      
	 
	 mov r6, r1;			  @ Add the two words without carry for the LSW.
	 bl load_var;			 
	 adds r5, r5, r6;	 	  
	 mov r6, r1; 
	 bl store_var;			  @ 32-bit add Add word 0, set status register
	 
	 mrs r7, CPSR;			 
	 subs r1, r1,#4;		  @ Decrement index
	 msr CPSR,r7;
	 
loop128:
	 msr CPSR,r7;
	 mov r6, r1;			  @ We add all other words using a carry.
	 bl load_var;			  @ We set the status register for subsequent operations
	 adcs r5, r5, r6;	 	  @ 32-bit add Add word n, set status register
	 mov r6, r1;
	 bl store_var; 
	
	 mrs r7, CPSR;
	 subs r1, r1,#4;		  @ Decrement to next word
	 cmp r0, r1;
	 bne loop128;			  @ Loop to add rest of words
	
	 msr CPSR,r7;
	 pop {r1,lr};
	 mov pc, lr;	 	      @ Return from subroutine to main loop

load_var:				     ;@ Subroutine to load two words from the variables into memory
	 ldr r5, [r2, r6];		  @ Load the value of var_a
	 ldr r6, [r3, r6];		  @ Load the value of var_b
	 mov pc, lr;	 	 	  @ Return from subroutine
	
store_var:                   ;@ Subroutine to shift move var_b into var_a and store the result of the add.
	 ldr r12,[r3, r6]; 		  @ Move var_b ...
	 str r12,[r2, r6]; 		  @ Into var_a
	 str r5, [r3, r6];	      @ Store the result into var_b
	 mov pc, lr;	 	 	  @ Return from subroutine

Final_OF:					 ;@ Deal with Final Overflow 
	 push {r0-r1};			  @ Store Overflow bit into OF_bit
	 ldr r0, =OF_bit;
	 mov r1, #1;
	 str r1, [r0, #0];
	 pop {r0-r1};
	 
	 ldr r7, =index_msb;	  @ Store Index lower (MSB)
	 str r0, [r7, #0];
	 mov r0, r3;
	 mov r1, r4;

Restore_R:					     ;@<Restore registers, and load LR into PC> 
	 ldmia r13!, {r2-r12, lr};    @ Load Multiple, Increment SP after, update
	 push {r2-r12, lr};
	
	 mrs r7, CPSR;			
	 subs r2, r2, r1;		  @ Compute Output n
	 ldr r1, =var_n;		 
	 str r2, [r1, #0];		  @ Store Output n into var_n
	 msr CPSR, r7;
	 
	 pop {r2-r12, lr};
	 mov pc, lr ;
	 
Compare:					 ;@ Check for special cases
	 push {r0,r1};
	 cmp r0, #0;              @ N=0
	 beq Return0;			  @ Return 0
	 cmp r0, #1;              @ N=1
	 beq Return1;			  @ Return 1
	 cmp r0, #2;			  @ N=2
	 beq Return1;			  @ Return 1
	 adds r1, r1, #1;         @ Turn off C, Z flags  
     pop {r0,r1};
	 bx lr;

test:
	 push {r0-r12,lr};
	 mrs r11, CPSR;
	 ldr r0, =var_n;		  @ Load Values
	 ldr r0, [r0, #0]; 		  @ Load Ouput n
	 ldr r1, =var_b;
	 ldr r2, =index_msb;	  @ Compare with -4 (occurs during final overflow)
	 ldr r2, [r2, #0];
	 
	 cmp r2, #500;			  @ If more than 4 words are used 
	 addne r2, r2, #4;		  @ Increment lower index
	 ldr r1, [r1, r2];        @ Load MSB
	 ldr r2, =var_b;
	 ldr r2, [r2, #508];	  @ Load LSB
	 
	 ldr r3, =OF_bit; 
	 ldr r3, [r3, #0];
	  
	 ldr r4, =ans_n;		  @ Load Test Case 
	 ldr r5, =ans_msw;
	 ldr r6, =ans_lsw;
	 ldr r7, =ans_of;
	 ldr r4, [r4, r12];
	 ldr r5, [r5, r12];
	 ldr r6, [r6, r12];
	 ldr r7, [r7, r12];
	 
	 cmp r0, r4;			  @ Compare Input with output
	 bne Error_ans;
	 cmp r1, r5;			  @ Compare MSB
	 bne Error_ans;
	 cmp r2, r6;			  @ Compare LSB
	 bne Error_ans;
	 cmp r3, r7;		      @ Compare Over flow
	 bne Error_ans;
	
	 msr CPSR, r11;
	 pop {r0-r12,lr};
	 
	 push {r0-r12,lr};		  @ Reset memory For next test case
	 mrs r11, CPSR;
	 str r12, [r1, #0];
	 ldr r1, =var_a;
	 ldr r2, =index_msb;
	 ldr r2, [r2, #0];
	 mov r3, #508;
	 mov r4, #0;
	 
Reset_Loop:
	 str r4, [r0, r3];		  @ Set value of 0 into each word in var_a
	 str r4, [r1, r3];		  @ Set value of 0 into each word in var_b
	 subs r3, r3, #4;
	 cmp r3, r2;
	 bne Reset_Loop;	
	 msr CPSR, r11;
	 pop {r0-r12,lr};		  @ End of Reset memory
	 
	 push {r11};
	 mrs r11, CPSR;			  @ Increment to next Test Case
	 adds r12, r12, #4;
	 msr CPSR, r11;
	 pop {r11};
	 
	 cmp r12, #40;
	 beq stop;
	 b main_loop;

Return0:				     ;@ Input n=0, return 0;
     pop {r0,r1};
	 str r2, [r1, #0];
	 ldr r0, =var_b;
	 mov r2, #0;
	 str r2, [r0, #508];
	 b test;

Return1:				     ;@ Input n=1 or 2, return 1;
     pop {r0,r1};
	 str r2, [r1, #0];
	 ldr r0, =var_b;
	 mov r2, #1;
	 str r2, [r0, #508];
	 b test;


;@ Test parameters 

.equ    TestCount,          7
;@  test number             0           4           8          12          16          20          24           28 			 32			   36;
test_n:   .word        		5,          1,         90,          0,          2,        186,        175,        1000,        9999,           50;	   @ input n
ans_n:    .word             5,          1,         90,          0,          2,        186,        175,        1000,        5901,           50;     @ output n
ans_of:   .word             0,          0,          0,          0,          0,          0,          0,           0,           1,            0;     @ overflow
ans_msw:  .word    0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0xFA63C8D9, 0x014219F1,  0x0021D8CB,  0x317429C5,   0x00000000;     @ fib msw
ans_lsw:  .word    0x00000005, 0x00000001, 0xA1BA7878, 0x00000000, 0x00000001, 0x333270F8, 0x792930BD,  0x5CC0604B,  0x38EA491F,   0xEE333961;     @ fib lsw	 


.data
var_n:      .space 4;    @ 1 word/32 bits – what Fib number ended up in var_b  (Fib+2)
var_a:      .space 512;  @ 4 words/128 bits
var_b: 		.space 512;  @ 4 words/128 bits
index_msb:  .space 4;    @ MSB Index
OF_bit:  	.space 4;    @ Overflow bit

.end;	 	 	         @ End of program	
