library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity sound3 is
	port (CLOCK_50, CLOCK2_50 			: in STD_LOGIC;
			AUD_ADCLRCK, AUD_DACLRCK 	: in STD_LOGIC;
			AUD_BCLK, AUD_ADCDAT 		: in STD_LOGIC;
			KEY 								: in STD_LOGIC_VECTOR(3 downto 0);
			SW 								: in STD_LOGIC_VECTOR(17 downto 0);
			LEDR 								: out STD_LOGIC_VECTOR(17 downto 0);
			LEDG 								: out STD_LOGIC_VECTOR(7 downto 0);
			FPGA_I2C_SDAT 					: inout STD_LOGIC;
			FPGA_I2C_SCLK 					: out STD_LOGIC;
			AUD_DACDAT, AUD_XCK 			: out STD_LOGIC);
end sound3;

architecture Behavior of sound3 is
 
	-- CODEC Cores.
	component clock_generator
	port (CLOCK2_50 : in STD_LOGIC;
			reset 	 : in STD_LOGIC;
			AUD_XCK 	 : out STD_LOGIC);
	end component;

	component audio_and_video_config
	port (CLOCK_50 : in STD_LOGIC;
			reset 	: in STD_LOGIC;
			I2C_SDAT : inout STD_LOGIC;
			I2C_SCLK : out STD_LOGIC);
	end component;
 
	component audio_codec
	port (CLOCK_50, reset, read_s, write_s 	: in STD_LOGIC;
			writedata_left, writedata_right 		: in STD_LOGIC_VECTOR(23 downto 0);
			AUD_ADCDAT, AUD_BCLK 					: in STD_LOGIC;
			AUD_ADCLRCK, AUD_DACLRCK 				: in STD_LOGIC;
			read_ready, write_ready 				: out STD_LOGIC;
			readdata_left, readdata_right 		: out STD_LOGIC_VECTOR(23 downto 0);
			AUD_DACDAT 									: out STD_LOGIC);
	end component;

	-- local signals and constants.
	signal read_ready, write_ready : STD_LOGIC;
	signal read_s, write_s : STD_LOGIC;
	signal writedata_left, writedata_right : STD_LOGIC_VECTOR(23 downto 0); 
	signal readdata_left, readdata_right : STD_LOGIC_VECTOR(23 downto 0); 
	signal reset : STD_LOGIC;
 
	type State is (Start, play, stop); --state enum
	signal currentSt : State; -- states
 
begin
	-- The audio core requires an active high reset signal
 
	reset <= not(KEY(3));
	read_s <= '0';
	LEDG(0) <= write_ready;
	LEDR <= SW;

	-- instantiate the parts of the audio core.
	my_clock_gen : clock_generator port map(CLOCK2_50, reset, AUD_XCK);

	cfg : audio_and_video_config port map(CLOCK_50, reset, FPGA_I2C_SDAT, FPGA_I2C_SCLK);
 
	codec : audio_codec port map( CLOCK_50, reset, read_s, write_s, writedata_left, writedata_right, AUD_ADCDAT, AUD_BCLK, AUD_ADCLRCK, AUD_DACLRCK, read_ready, write_ready, readdata_left, readdata_right, AUD_DACDAT);
 
	process (all)
		variable volume : signed (23 downto 0) := "000001000000000000000000";
		variable A, B, C, D, E, F, G, C5 : integer := 0;
		variable counter : integer := 0;
	begin
		if reset = '1' then
			currentSt <= Start;
		elsif rising_edge(CLOCK_50) then
 
			case currentSt is
 
				when start => 
					C := 168;
					currentSt <= play;
 
				when play => 
				
					if write_ready = '1' AND SW(17) = '1' then
						
						writedata_left <= std_logic_vector(volume);
						writedata_right <= std_logic_vector(volume);
						write_s <= '1';
 
						C := C - 1;
 
						if C = 0 then
							volume := -volume;
							C := 168;
						end if;
						
					elsif write_ready = '0' then
						write_s <= '0';
					end if;
					
						currentSt <= play;
						
				when others => currentSt <= Start;
 
			end case;
		end if;
 
	end process;

	end;