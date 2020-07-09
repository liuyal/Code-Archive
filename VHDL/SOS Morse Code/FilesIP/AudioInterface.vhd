Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity AudioInterface is
	Generic ( SID : integer := 100 ); 
	Port (
--		SW : in std_logic_vector(17 downto 0);
--		LEDR : out std_logic_vector(17 downto 0) := (others => '0');
--		LEDG : out std_logic_vector(8 downto 0 ) := (others => '0');
--		KEY : in std_logic_vector(3 downto 0);
		CLOCK_50 : in std_logic;
		init : in std_logic;

		I2C_SDAT : inout std_logic;
		I2C_SCLK, AudMclk : out std_logic;
		AUD_ADCDAT : in std_logic;
		AUD_DACDAT : out std_logic;
		AUD_ADCLRCK, AUD_DACLRCK, AUD_BCLK : in std_logic;
		
		SamClk : out std_logic;
		AudioIn : out signed(15 downto 0);
		AudioOut : in signed(15 downto 0)
);
End Entity AudioInterface;


Architecture Structural of AudioInterface is
	Component AudioSubSystemMono is
		Port (
			Clock_50 : in std_logic;
			AudMclk : out std_logic;
			Init : in std_logic;

			I2C_Sclk : out std_logic;
			I2C_Sdat : inout std_logic;
		
			Bclk, AdcLrc, DacLrc, AdcDat : in std_logic;
			DacDat : out std_logic;

			AudioOut : in signed(15 downto 0);
			AudioIn : out signed(15 downto 0);
			SamClk : out std_logic );
	End Component AudioSubSystemMono;

--	Signal AudioIn, AudioInL, AudioInR : signed(15 downto 0);
--	Signal AudioOut, AudioOutL, AudioOutR : signed(15 downto 0);
--	Signal SamClk : std_logic;
	Signal k0 : std_logic;

Begin
	Assert SID < 99999 and SID >= 0
	Report LF & LF
				& "Read The Lab Instructions - You must enter a value for SID in the top-level instance" & LF
				& "GENERIC MAP(SID => XXXXX)," & LF
				& "      where XXXXX is the last five digits of your student number" & LF
				& LF & LF
	Severity  failure;

-- SamClk may not exist before the Codec has been inititalised.
	k0 <= init when rising_edge(CLOCK_50);
--	k1 <= KEY(1) when rising_edge(CLOCK_50);
	
ASSM: AudioSubSystemMono port map (
			Clock_50 => CLOCK_50, AudMclk => AudMclk,	-- period is 80 ns ( 12.5 Mhz )
			Init => not k0, 									-- +ve edge initiates I2C data
			I2C_Sclk => I2C_SCLK,
			I2C_Sdat => I2C_SDAT,
			Bclk => AUD_BCLK, AdcLrc => AUD_ADCLRCK, DacLrc => AUD_DACLRCK,
			AdcDat => AUD_ADCDAT, DacDat => AUD_DACDAT,

			AudioOut => AudioOut, AudioIn => AudioIn, SamClk => SamClk );



End Architecture Structural;
