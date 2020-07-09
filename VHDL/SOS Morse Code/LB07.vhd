Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity LB07 is
	Port (
		SW : in std_logic_vector(17 downto 0);
		LEDR : out std_logic_vector(17 downto 0) := (others => '0');
		LEDG : out std_logic_vector(8 downto 0 ) := (others => '0');
		KEY : in std_logic_vector(3 downto 0);
		
		TEMP : out unsigned (5 downto 0);
		HEX3, HEX2, HEX1, HEX0 : out std_logic_vector(6 downto 0);
		
		CLOCK_50 : in std_logic;

		I2C_SDAT : inout std_logic;
		I2C_SCLK, AUD_XCK : out std_logic;
		AUD_ADCDAT : in std_logic;
		AUD_DACDAT : out std_logic;
		AUD_ADCLRCK, AUD_DACLRCK, AUD_BCLK : in std_logic );
End Entity LB07;


Architecture structural of LB07 is

	Signal AudioIn, AudioOut : signed(15 downto 0);
	Signal SamClk : std_logic;
	Signal Morse_wire : std_logic;
	Signal OpX, OpY, SUM : signed (3 downto 0);
	Signal S_wire, O_wire : std_logic_vector (6 downto 0);

Begin
--***********************************************************************************
-- You must enter the last five digits from the student number of one group member.
-- example: 

--		work.AudioInterface generic map ( SID => xxxxx ) - where xxxxx are the last 5 digits.
--
--***********************************************************************************
ASSM: Entity work.AudioInterface	generic map ( SID => 55583 )
			port map (
			Clock_50 => CLOCK_50, AudMclk => AUD_XCK,	-- period is 80 ns ( 12.5 Mhz )
			init => KEY(0), 									-- +ve edge initiates I2C data
			I2C_Sclk => I2C_SCLK,
			I2C_Sdat => I2C_SDAT,
			AUD_BCLK => AUD_BCLK, AUD_ADCLRCK => AUD_ADCLRCK, AUD_DACLRCK => AUD_DACLRCK,
			AUD_ADCDAT => AUD_ADCDAT, AUD_DACDAT => AUD_DACDAT,

			AudioOut => AudioOut, AudioIn => AudioIn, SamClk => SamClk );

	--AudioOut <= AudioIn;
	
--***********************************************************************************


	
--***********************************************************************************
	-- PART 2
--***********************************************************************************
	--OpX <= signed(SW(7 downto 4));
	--OpY <= signed(SW(3 downto 0));
	--SUM <= OpX + OpY;
	--LEDR(3 downto 0)<= std_logic_vector(SUM);
--***********************************************************************************
	

	Test: Entity work.ToneGenerator port map (
			Freq => unsigned(SW (15 downto 0)), clear => NOT ( NOT Morse_wire OR KEY(1)), WaveOut => AudioOut, clk => SamClk );
	
--***********************************************************************************
	-- PART 3
--***********************************************************************************
	
	
	
	Morse: Entity work.MorseGenerator port map ( 
			Morse_clk => SamClk, PulseOut => Morse_wire, Pulse_6 => TEMP);
			
			
		HEX2 <= "0010010" WHEN Morse_wire = '1' Else "1111111" WHEN Morse_wire = '0';
		
		HEX1 <= "1000000" WHEN Morse_wire = '1' Else "1111111" WHEN Morse_wire = '0';
		
		HEX0 <= "0010010" WHEN Morse_wire = '1' Else "1111111" WHEN Morse_wire = '0';
		
		HEX3 <= "1111111";
	
	LEDG (8) <= Morse_wire;
	LEDG (7) <= Morse_wire;
	LEDG (6) <= Morse_wire;
	LEDG (5) <= Morse_wire;
	LEDG (4) <= Morse_wire;
	LEDG (3) <= Morse_wire;
	LEDG (2) <= Morse_wire;
	LEDG (1) <= Morse_wire;
	LEDG (0) <= Morse_wire;
	
	LEDR (17) <= Morse_wire;
	LEDR (16) <= Morse_wire;
	LEDR (15) <= Morse_wire;
	LEDR (14) <= Morse_wire;
	LEDR (13) <= Morse_wire;
	LEDR (12) <= Morse_wire;
	LEDR (11) <= Morse_wire;
	LEDR (10) <= Morse_wire;
	LEDR (9) <= Morse_wire;
	LEDR (8) <= Morse_wire;
	LEDR (7) <= Morse_wire;
	LEDR (6) <= Morse_wire;
	LEDR (5) <= Morse_wire;
	LEDR (4) <= Morse_wire;
	LEDR (3) <= Morse_wire;
	LEDR (2) <= Morse_wire;
	LEDR (1) <= Morse_wire;
	LEDR (0) <= Morse_wire;
	
End Architecture structural;
