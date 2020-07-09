/* Linker script to configure memory regions. */
MEMORY
{
  FLASH (rx) : ORIGIN = 0x00000000, LENGTH = 0x20000   /* 128 KiB */
  RAM (rwx)  : ORIGIN = 0x40000000, LENGTH = 0x04000   /*  16 KiB */
}
ENTRY(Reset_Handler)

SECTIONS
{
	.text :
	{
		*(.text*)
		*(.rodata*)
	} > FLASH

	.data :
	{
		__data_start__ = .;
		*(.data*)
		. = ALIGN(4);
		/* All data end */
		__data_end__ = .;

	} > RAM
}
