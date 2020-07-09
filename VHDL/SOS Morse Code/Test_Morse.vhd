Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity Test_Morse is
	Port (
			LEDG : out std_logic_vector(8 downto 0 ):= (others => '0');
			TEMP : out unsigned (5 downto 0);
			CLOCK_50 : in std_logic
		);
End Entity Test_Morse;


Architecture COND of Test_Morse is

		Signal Morse_wire : std_logic;

begin

	Morse: Entity work.MorseGenerator port map (
	Morse_clk => CLOCK_50, PulseOut => Morse_wire, Pulse_6 => TEMP);
	
	LEDG (0) <= Morse_wire;

End COND;