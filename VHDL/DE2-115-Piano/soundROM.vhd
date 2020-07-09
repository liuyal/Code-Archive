library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity soundROM is
	port (CLOCK_50, CLOCK2_50 			: in STD_LOGIC;
			AUD_ADCLRCK, AUD_DACLRCK 	: in STD_LOGIC;
			AUD_BCLK, AUD_ADCDAT 		: in STD_LOGIC;
			KEY 								: in STD_LOGIC_VECTOR(3 downto 0);
			SW 								: in STD_LOGIC_VECTOR(17 downto 0);
			LEDR 								: out STD_LOGIC_VECTOR(17 downto 0);
			LEDG 								: out STD_LOGIC_VECTOR(7 downto 0);
			HEX7, HEX6, HEX5, HEX4		: out STD_LOGIC_VECTOR(6 downto 0);
			I2C_SDAT 						: inout STD_LOGIC;
			I2C_SCLK 						: out STD_LOGIC;
			AUD_DACDAT, AUD_XCK 			: out STD_LOGIC);
end soundROM;

architecture Behavior of soundROM is
 
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
	
	component data
	PORT (address		: IN STD_LOGIC_VECTOR (7 DOWNTO 0);
			clock		: IN STD_LOGIC  := '1';
			q		: OUT STD_LOGIC_VECTOR (7 DOWNTO 0));
	end component;

	-- local signals and constants.
	signal read_ready, write_ready : STD_LOGIC;
	signal read_s, write_s : STD_LOGIC;
	signal writedata_left, writedata_right : STD_LOGIC_VECTOR(23 downto 0); 
	signal readdata_left, readdata_right : STD_LOGIC_VECTOR(23 downto 0); 
	signal reset : STD_LOGIC;
	signal input : unsigned (7 downto 0);
	
	signal address, q : STD_LOGIC_VECTOR(7 downto 0); 
	signal clock : std_LOGIC;
	
	signal index : unsigned (7 downto 0) := (others => '0');
	signal send : std_LOGIC;
	
	type State is (start, init, calc1, calc2, play, stop); --state enum
	signal currentSt : State; -- states
 
begin
	-- The audio core requires an active high reset signal
 
	reset <= not(KEY(3));
	read_s <= '0';
	
	LEDG(0) <= write_ready;
	LEDR(7 downto 0) <= q;
	LEDR(17 downto 10) <= STD_LOGIC_VECTOR(index);
	input <= unsigned(q);
	
	BCD7: Entity work.digit7seg port map (STD_LOGIC_VECTOR(index(7 downto 4)),HEX7);
	BCD6: Entity work.digit7seg port map (STD_LOGIC_VECTOR(index(3 downto 0)),HEX6);
	
	BCD5: Entity work.digit7seg port map (STD_LOGIC_VECTOR(q(7 downto 4)),HEX5);
	BCD4: Entity work.digit7seg port map (STD_LOGIC_VECTOR(q(3 downto 0)),HEX4);
	
	-- instantiate the parts of the audio core.
	my_clock_gen : clock_generator port map(CLOCK2_50, reset, AUD_XCK);

	cfg : audio_and_video_config port map(CLOCK_50, reset, I2C_SDAT, I2C_SCLK);
 
	codec : audio_codec port map( CLOCK_50, reset, read_s, write_s, writedata_left, writedata_right, 
	AUD_ADCDAT, AUD_BCLK, AUD_ADCLRCK, AUD_DACLRCK, read_ready, write_ready, readdata_left, readdata_right, AUD_DACDAT);
 
	dataga : data port map (STD_LOGIC_VECTOR(index), send, q);
 
	process (all)
		variable volume : signed (23 downto 0) := (others => '0');
		variable amplitude : signed (23 downto 0) := (others => '0');
		variable A, B, C, D, E, F, G, C5 : integer := 0;
		variable Av, Bv, Cv, Dv, Ev, Fv, Gv, C5v : signed (23 downto 0) := (others => '0');
		variable AB, CD, EF, GC5, ABCD, EFGC5 : signed (23 downto 0) := (others => '0');
		variable counter : unsigned (25 downto 0)  := (others => '0');
		variable i : unsigned (7 downto 0) := (others => '0');
	begin
		if reset = '1' then
			currentSt <= Start;
		elsif rising_edge(CLOCK_50) then
			case currentSt is
			
				when start => 
					C := 2*168;
					D := 2*150;
					E := 2*133;
					F := 2*126;
					G := 2*112;
					A := 2*100;
					B := 2*89;
					C5 := 2*84;
					volume(14) := '1';
					amplitude := (others => '0');
					counter := (others => '0');
					i := (others => '0');
					index <= (others => '0');
					send <= '0';
					currentSt <= init;
				
				when init =>
				
					if input = 1 then Cv := volume; --C
						if C <= 168 then 
							Cv := -volume; 
						end if;
					else Cv := (others => '0'); end if;
					
					if input = 2 then Dv := volume; --D
						if D <= 150 then 
							Dv := -volume; 
						end if;
					else Dv := (others => '0'); end if;
					
					if input = 3 then Ev := volume; --E
						if E <= 133 then 
							Ev := -volume; 
						end if;
					else Ev := (others => '0'); end if;
					
					if input = 4 then Fv := volume; --F
						if F <= 126 then 
							Fv := -volume; 
						end if;
					else Fv := (others => '0'); end if;
					
					if input = 5 then Gv := volume; --G
						if G <= 112 then 
							Gv := -volume; 
						end if;
					else Gv := (others => '0'); end if;
					
					if input = 6 then Av := volume; --A
						if A <= 100 then 
							Av := -volume; 
						end if;
					else Av := (others => '0'); end if;
					
					if input = 7 then Bv := volume; --B
						if B <= 89 then 
							Bv := -volume; 
						end if;
					else Bv := (others => '0'); end if;	
					
					if input = 8 then C5v := volume; --C5
						if C5 <= 84 then 
							C5v := -volume; 
						end if;
					else C5v := (others => '0'); end if;

					currentSt <= calc1;
				
				when calc1 =>
					AB := Av + Bv;
					CD := Cv + Dv;
					EF := Ev + Fv;
					GC5 := Gv + C5v;
					currentSt <= calc2;
					
				when calc2 =>
					ABCD := AB + CD;
					EFGC5 := EF + GC5;
					currentSt <= play;
					
				when play => 
					if write_ready = '1' then
						
						amplitude := ABCD + EFGC5;
						writedata_left <= std_logic_vector(amplitude);
						writedata_right <= std_logic_vector(amplitude);
						write_s <= '1';
						
						C := C - 1; D := D - 1; E := E - 1; F := F - 1;
						G := G - 1; A := A - 1; B := B - 1; C5 := C5 - 1;
													
						if C <= 0 then C := 2*168; end if;
						if D <= 0 then D := 2*150; end if;
						if E <= 0 then E := 2*133; end if;
						if F <= 0 then F := 2*126; end if;
						if G <= 0 then G := 2*112; end if;
						if A <= 0 then A := 2*100; end if;							
						if B <= 0 then B := 2*89; end if;
						if C5 <= 0 then C5 := 2*84; end if;
						
					elsif write_ready = '0' then
						write_s <= '0';
					end if;
					
					if counter(22) = '1' then				
						counter := (others => '0');
						i := i + 1;
						if i > 26 then i := (others => '0'); end if;
						send <= '0';
						currentSt <= stop;
					else 
						counter := counter + 1;
						send <= '1';
						currentSt <= init;					
					end if;
					
					ledg(1) <= '0';
					index <= i;
				
				when stop =>
					ledg(1) <= '1';
					if counter(20) = '1' then
						counter := (others => '0');
						currentSt <= init;
					else
						counter := counter + 1;
						currentSt <= stop;
					end if;
					
				when others => currentSt <= start;
 
			end case;
		end if;
 
	end process;

	end;