Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity ClockGen is
	Port (
		MainClk : in std_logic;
		I2CClk, AudMclk : out std_logic );
End Entity ClockGen;

Architecture dataflow of ClockGen is
	Signal DivChain : unsigned( 26 downto 0 );
-- Number of 20 ns clocks for each state of I2CTx CU.
	Constant	Period : integer := 64;
	Constant	PWidth : integer := 16;
Begin
--Modulo M synchronous counter for clock generation.
CB:Block ( rising_edge( MainClk ) )
	Begin
		DivChain <= guarded ( others => '0' ) when DivChain >= Period-1 else DivChain + 1;
	End Block CB;
	I2CClk <= '1' when DivChain < PWidth else '0'; --this should be registered to avoid glitches.

	AudMclk <= DivChain(1); -- is 12.5 Mhz, 50% duty cycle
End Architecture dataflow;

Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity Synchroniser is
	Port (
		MainClock : in std_logic;
		BclkIn,  AdcLrcIn,  DacLrcIn,  AdcDatIn  : in Std_logic;
		BclkOut, AdcLrcOut, DacLrcOut, AdcDatOut : out Std_logic	);
		
		attribute	useioff : boolean;
		attribute	useioff of AdcLrcIn : signal is true;
		attribute	useioff of DacLrcIn : signal is true;
		attribute	useioff of BclkIn : signal is true;
		attribute	useioff of AdcDatIn : signal is true;
		
End Entity Synchroniser;

Architecture rtl of Synchroniser is
Begin
-- Could introduce a noise spike filter here. Will do later if necessary.

	BclkOut <= BclkIn when Rising_Edge( MainClock );
	AdcLrcOut <= AdcLrcIn when Rising_Edge( MainClock );
	DacLrcOut <= DacLrcIn when Rising_Edge( MainClock );
	AdcDatOut <= AdcDatIn when Rising_Edge( MainClock );
	
-- Should assign these to clock buffers. I need to determine how to force
-- Quartus to use the IO F/Fs for the synchroniser and also to assign
-- signals to global clock networks. Will do this later.

End Architecture rtl;