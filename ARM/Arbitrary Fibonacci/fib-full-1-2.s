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
;@ Name        : fib-full-1-2.s
;@ Description : Submission for Assignment 1.
;@============================================================================

.text; 				          @ Store in ROM

Reset_Handler:

.global Reset_Handler; 		  @ The entry point on reset
					 	
main:						 ;@ The main program	

	ldr sp, =#0x40004000	 ;@ Initialize SP just past the end of RAM
	mov r4, #3;               @ Some value I care about.
NextT:
	ldr r0, =test_n;
	ldr r0, [r0, r1];         @ Load value of N into first argument (Load Test)
	bl compare;
	bl sub_fib;               @ Find Nth value of the Fibonacci sequence	
	
stop: 						 ;@ at this point, r4 should be 3
	 b stop;
Error_ans:
	 b Error_ans;

sub_fib:
	 push {r1-r12,lr};       @<Store register(s) and LR to stack>
	 
	 ldr r2, =var_a;		 @ Pointers to the variables
	 ldr r3, =var_b;
	 ldr r4, =var_OF;	     @ Load a 128-bit 1 into both variables	 
	 
	 push {r1};
	 ldr r1, =var_n;		 @ Store output n, if overflow replace output n
	 str r0, [r1, #0];
	 pop {r1};
	 
	 mov r12, #0;		  	 @ Constant used for initializing the variables
	 str r12, [r4, #0];
	 str r12, [r2, #0];	     @ Set the value of var_a
	 str r12, [r3, #0];	 	 @ Set the value of var_b
	 str r12, [r2, #4];	 	 @ Complete the initialization for var_a and var_b
	 str r12, [r3, #4];
	 str r12, [r2, #8];
	 str r12, [r3, #8];
	 mov r12, #1;		 	 @ Constant used for initializing LSW of variables
	 str r12, [r2, #12];
	 str r12, [r3, #12];
	 mrs r4, CPSR;
	 subs r0, r0, #2;		  @ Decrement by 2 to calculate nth fib number
	 msr CPSR,r4;
	 mov r4, r0;		 	 @ Select which term we are calculating
	 
loop:	 
	 bl add_128;	 	 	 @ Perform a 128-bit add
	 bcs overflow;	 	 	 @ Detect if variable overflowed by looking
	 						;@ at the carry flag after the top word add; If so, branch to "overflow"
	 subs r4, r4, #1;		 @ Decrement the loop counter
	 bne loop;	 	 		 @ Reached the desired term
	 	 
	 pop {r1-r12,lr};        @<Restore registers, and load LR into PC>

test:
	 push {r1-r12,lr};		 @ Load Test cases and compare
	 mrs r8, CPSR;
	 mov r12, r1;
	 ldr r0, =var_n;		 @ Load calculated cases
	 ldr r0, [r0, #0];
	 ldr r1, =var_b;
	 ldr r2, [r1, #12];		 @ Load LSB
	 ldr r1, [r1, #0];		 @ Load MSB
	 ldr r3, =var_OF;
	 ldr r3, [r3, #0]; 
	 
	 ldr r4, =ans_n;		 @ Load Test Case answers
	 ldr r4, [r4, r12];
	 ldr r5, =ans_msw;
	 ldr r5, [r5, r12];
	 ldr r6, =ans_lsw;
	 ldr r6, [r6, r12]; 
	 ldr r7, =ans_of;
	 ldr r7, [r7, r12];
	 
	 cmp r0, r4;			  @ Compare Input with output
	 bne Error_ans;
	 cmp r1, r5;			  @ Compare MSB
	 bne Error_ans;
	 cmp r2, r6;			  @ Compare LSB
	 bne Error_ans;
	 cmp r3, r7;		      @ Compare Over flow
	 bne Error_ans;
	 
	 msr CPSR, r8;
	 pop {r1-r12,lr}; 
	 
	 push {r11};
	 mrs r11, CPSR;			 @ Increment to next Test Case
	 adds r1, r1, #4;
	 msr CPSR, r11;
	 pop {r11};
	 
	 push {r0-r12};	
	 mov r1, #12;	 	     @ Clear memory for next test
	 
clear_loop:
	 ldr r2, =var_a;		 
	 ldr r3, =var_b;
	 mov r12, #0;		  	 @ Set to 0
	 str r12, [r3, r1];
	 str r12, [r2, r1];	     
	 subs r1, r1, #4;
	 bne clear_loop;
	 pop {r0-r12};
	 
	 cmp r1, #32;
	 beq stop;				 @ If all tests are done brance to stop
	 b NextT;

overflow:					;@ Oops, the add overflowed the variable! 
	 ldr r0, =var_n;
	 mov r1, #0;
	 str r1, [r0, #0];
	 str r4, [r0, #0];
	 
	 mov r0, #1;
	 ldr r1, =var_OF;
	 str r0, [r1, #0];
	 
	 pop {r1-r12,lr};
	 push {r1-r12};
	 
	 ldr r0, =var_n;		 @ Calculate the n that the overflow occured at and store into var_n
	 mov r2, r1;
	 ldr r1, =test_n;
	 ldr r1, [r1, r2];
	 ldr r2, [r0, #0];
	 
	 mrs r11, CPSR;
	 subs r1, r1, r2;
	 msr CPSR, r11;
	 str r1, [r0, #0];
	 
	 pop {r1-r12};
	 b test;
	 
add_128:					;@ Subroutine to load two words from the variables into memory
	 push {lr};				 @ Start with the least significant word (word 0)	
	  			            ;@ Add the two words without carry for the LSW.
	 mov r1, #12;			 @ Add all other words using a carry.
	 bl load_var;	 		 @ Set the status register for subsequent operations
	 adds r0, r0, r1;	 	 @ 32-bit add Add word 0, set status register
	 mov r1, #12;
	 bl store_var;
	 
	 mov r1, #8;
	 bl load_var;	 
	 adcs r0, r0, r1;	 	 @ 32-bit add Add word 1 with carry, set status register
	 mov r1, #8;
	 bl store_var;
	 
	 mov r1, #4; 			  
	 bl load_var;
	 adcs r0, r0, r1;	 	 @ 32-bit add Add word 2 with carry, set status register
	 mov r1, #4;
	 bl store_var;
	 
	 mov r1, #0;
	 bl load_var;
	 adcs r0, r0, r1;	 	 @ 32-bit add Add word 3 with carry, set status register
	 mov r1, #0;
	 bl store_var;			 @ Complete the 128-bit add	
	 
	 pop {pc};				 @ Return from subroutine
	
load_var:				   ;@ Subroutine to load two words from the variables into memory
						   ;@ Update this subroutine to take an argument so it can be reused for loading all four words
	 ldr r0, [r2, r1];		@ Load the value of var_a
	 ldr r1, [r3, r1];		@ Load the value of var_b
	 mov pc, lr;	 	 	@ Return from subroutine
	
store_var:                 ;@ Subroutine to shift move var_b into var_a and store the result of the add.
						   ;@ Update this subroutine to take an argument so it can be reused for storing all four words
	 ldr r12,[r3, r1]; 		@ Move var_b ...
	 str r12,[r2, r1]; 		@    ... into var_a
	 str r0, [r3, r1];	    @ Store the result into var_b
	 mov pc, lr;	 	 	@ Return from subroutine	 

compare:					 ;@ Check for special cases
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

Return0:				    ;@ Input n=0, return 0;
     pop {r0,r1};
	 push {r1};
	 ldr r1, =var_n;		 @ Store output n
	 str r0, [r1, #0];
	 pop {r1};
	 push {r0-r2};
	 ldr r0, =var_b;		 @ Store fib number
	 mov r2, #0;
	 str r2, [r0, #12];
	 pop {r0-r2};
	 b test;

Return1:				    ;@ Input n=1 or 2, return 1;
     pop {r0,r1};
	 push {r1};
	 ldr r1, =var_n;		 @ Store output n
	 str r0, [r1, #0];
	 pop {r1};
	 push {r0-r2};
	 ldr r0, =var_b;		 @ Store fib number
	 mov r2, #1;
	 str r2, [r0, #12];
	 pop {r0-r2};
	 b test; 


;@ Test parameters format 2
.equ    TestCount,    7
;@    test number           0           4           8           12         16          20          24 		   28
test_n:   .word             5,          1,         90,          0,          2,       1000,        175,         50;    @ input n
ans_n:    .word             5,          1,         90,          0,          2,        186,        175,         50;    @ output n
ans_of:   .word             0,          0,          0,          0,          0,          1,          0,          0;    @ overflow
ans_msw:  .word    0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x9523A14F, 0x014219F1, 0x00000000;    @ fib msw
ans_lsw:  .word    0x00000005, 0x00000001, 0xA1BA7878, 0x00000000, 0x00000001, 0x1AAB3E85, 0x792930BD, 0xEE333961;    @ fib lsw

.data;	 	 	 	 	 @ Store in RAM	 	 
var_n:   .space  4;
var_a:	 .space 16;	 	 @ Variable A (128-bit)
var_b:	 .space 16;	 	 @ Variable B (128-bit)
var_OF:  .space  4;
.end;	 	 	 		 @ End of program	 
