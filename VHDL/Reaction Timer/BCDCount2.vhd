LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY BCDCount2 IS
PORT (
		Clock : in std_logic;
		Clear : in std_logic;
      Enable : in std_logic;
		BCD0, BCD1 : out std_LOGIC_vector (3 downto 0)
);
END ENTITY BCDCount2;

ARCHITECTURE Behaviour OF BCDCount2 IS

	Signal zero : std_LOGIC_vector (3 downto 0);

	Signal wireA, wireB, A, B : std_logic;
	
	Signal outA, outB : std_LOGIC_vector (3 downto 0);

	Signal Enable_wireA, Enable_wireB : std_logic;

Begin
	
	zero <= "0000";

	Enable_wireA <= '1' When Enable = '1' Else '0';
	Enable_wireB <= WireA When Enable = '1' Else '0';
	
	A <= Clear OR wireA;
	obj1 : EntITY work.Count4 Port map (
	clk_in_count4 => Clock, Loads => A, Enb => Enable_wireA, D => zero, Q => outA);
	
	wireA <= outA(0) AND outA(3);
	
	B <= Clear OR wireB;
	obj2 : EntITY work.Count4 Port map (
	clk_in_count4 => Clock, Loads => B, Enb => Enable_wireB, D => zero, Q => outB);
	
	wireB <= outB(0) AND outB(3) AND wireA;
	
	BCD0 <= outA;
	BCD1 <= outB;


END Behaviour;




