LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY TestReaction IS
PORT (
	Clk_in : in std_logic;
	SW : in std_logic_vector (17 downto 0);
	KEY : in std_logic_vector (3 downto 0);
	LEDR : out std_logic_vector (17 downto 0);
	HEX1, HEX0 : out std_logic_vector (6 downto 0)


);
END ENTITY TestReaction;

ARCHITECTURE Behaviour OF TestReaction IS

	Signal Clk_wire : std_logic;
	Signal PSW_wire : std_logic;
	Signal LED_wire : std_logic;
	signal A,B,w, Reset : std_logic;

	Signal BCD1_out, BCD0_out : std_logic_vector (3 downto 0);


Begin

	PSW_wire <= KEY(0);
	Reset <= SW(16);
	
	
	presclae_clock : entity work.PreScale Port Map(clk_in_pre => Clk_in, clk_out => clk_wire,
	count_enb=> SW(17), Aclear => Reset);
	
	LED_wire <= A when rising_edge(clk_wire);

	B <= '1' When SW(17) = '1' else LED_wire;	-- MUX
	
	A <= B AND PSW_wire;	--AND GATE
	
	LEDR(0) <= Not LED_wire;

	BCDCOUNT : entity work.BCDCount2 Port Map(
	clock => clk_wire, Enable => LED_wire, clear => Reset,
	BCD1 => BCD1_out, BCD0 => BCD0_out);
	
	Seg0 : entity work.SegDecoder Port Map(D => BCD0_out, Y => HEX0);
		
	Seg1 : entity work.SegDecoder Port Map(D => BCD1_out, Y => HEX1);



END Behaviour;




