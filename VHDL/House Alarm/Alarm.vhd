LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY Alarm IS

PORT (
		Enable : in std_logic;
		Alarm_Clk : in std_logic;
		Seg2, Seg1, Seg0 : out std_logic_vector (6 downto 0) 
);
END ENTITY Alarm;

ARCHITECTURE Behaviour OF Alarm IS

	Signal Nine : std_logic_vector (6 downto 0):= "0011000";
	Signal One : std_logic_vector (6 downto 0):= "1111001";
	Signal None : std_logic_vector (6 downto 0):= "1111111";
	
	Signal Mux_nine,Mux_one1, Mux_one2: std_logic_vector (6 downto 0);
	Signal X, Y, Z: std_logic_vector (6 downto 0);
	
	Signal Slow_clk : std_logic;

	
BEGIN
	
	Slow_clk <= Alarm_Clk;
	
	Mux_nine <= Nine When Enable = '1' else None When Enable = '0';
	Mux_one1 <= One When Enable = '1' else None When Enable = '0';
	Mux_one2 <= One When Enable = '1' else None When Enable = '0';

	X <= Mux_nine;
	Y <= Mux_one1;
   Z <= Mux_one2;
	
	Seg2 <= X When Slow_clk = '1' else None;
	
	Seg1 <= Y When Slow_clk = '1' else None;
	
	Seg0 <= Z When Slow_clk = '1' else None;


END Behaviour;