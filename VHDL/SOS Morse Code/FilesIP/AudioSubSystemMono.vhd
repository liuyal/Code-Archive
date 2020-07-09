Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Library altera;
use altera.altera_primitives_components.all;


Entity AudioSubSystemMono is
	Port (
		Clock_50 : in std_logic;
		AudMclk : out std_logic;
		Init : in std_logic; --  +ve edge initiates I2C data.

		I2C_Sclk : out std_logic;
		I2C_Sdat : inout std_logic;
		
		Bclk, AdcLrc, DacLrc, AdcDat : in std_logic; -- inputs from pins
		DacDat : out std_logic;

		AudioOut : in signed(15 downto 0);
		AudioIn : out signed(15 downto 0);
		SamClk : out std_logic );
End Entity AudioSubSystemMono;

Architecture Structural of AudioSubSystemMono is
	Signal I2CClk : std_logic;
	Signal Sdout, Sdin, Sclk : std_logic;
	Signal BclkS, AdcLrcS, DacLrcS, AdcDatS : std_logic; -- synchronised nodes.

	Signal LStreamIN, LStreamOUT, RStreamIN, RStreamOUT : signed( 31 downto 0 );
	Signal Ch0In, Ch1In, Ch0Out, Ch1Out : signed(15 downto 0);
	Signal Ch0InAlign : signed(15 downto 0);
	Signal AddOut : signed(16 downto 0);
Begin

CG: 	Entity Work.ClockGen port map (Clock_50, I2CClk, AudMclk);
SYN:	Entity Work.Synchroniser port map (
				MainClock => CLOCK_50,
				BclkIn => Bclk, BclkOut => BclkS,
				AdcLrcIn => AdcLrc, AdcLrcOut => AdcLrcS,
				DacLrcIn => DacLrc, DacLrcOut => DacLrcS,
				AdcDatIn => AdcDat, AdcDatOut => AdcDatS );

--****************************************************************************
-- The I2C system initializes the Codec.
--****************************************************************************
	I2C_Sclk <= Sclk;
	Sdin <= I2C_SDat;
	ODB: OPNDRN port map (a_in => Sdout, a_out => I2C_SDat);
CI: Entity Work.CodecInit port map ( ModeIn => "10",
							I2CClk => I2CClk, Sclk => Sclk, Sdin => Sdin, Sdout => Sdout,
							Init => Init,	SwitchWord => (others=>'0') );

							
--****************************************************************************
-- The Audio interface to the Codec..
--****************************************************************************
AI: Entity Work.AudRx
		port map ( Bclk => BclkS , AdcLrc => AdcLrcS,	AdcDat => AdcDatS,
					  LAudio => LStreamIN, RAudio => RStreamIN );
AO: Entity Work.AudTx
		port map ( Bclk => BclkS , DacLrc => DacLrcS, DacDat => DacDat,
					  LAudio => LStreamOUT, RAudio => RStreamOUT );

--*********************************************************************	
-- Entity Intermediate Audio Processing.
-- Assume 2 Channels, 16-bit sample words at 50 kSPS	
-- Assume that both input and output have the same sample rates.
--*********************************************************************
	Ch0In <= LStreamIN(31 downto 16);
	Ch1In <= RStreamIN(31 downto 16);
	LStreamOUT(31 downto 16) <= Ch0Out;
	RStreamOUT(31 downto 16) <= Ch1Out; 
	LStreamOUT(15 downto 0) <= (others => '0');								
	RStreamOUT(15 downto 0) <= (others => '0');

	SamClk <= AdcLrcS; -- Clock from ADC after the sychroniser.

--align so that both channels change on the +ve edge of SamClk
-- sign-extend add and then truncate the last bit.	
	Ch0InAlign <= Ch0In when Rising_Edge(AdcLrc);
	AddOut <= (Ch0InAlign(15) & Ch0InAlign) + (Ch1In(15) & Ch1In);
	AudioIn <= Addout(16 downto 1);
	
	Ch0Out <= AudioOut;
	Ch1Out <= AudioOut;

End Architecture Structural;