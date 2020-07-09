LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
Use ieee.numeric_std.all;

ENTITY BCD IS
PORT (
	BCD_in : in std_LOGIC_vector  (5 downto 0);
	
	Bout : out std_LOGIC_vector  (7 downto 0)
);
END ENTITY BCD;

ARCHITECTURE Behaviour OF BCD IS
		
		Signal temp : unsigned(5 downto 0);
		
		signal A : unsigned (6 downto 3);
		signal B : unsigned (3 downto 0);
		signal C : unsigned (3 downto 0);
		signal D : unsigned (3 downto 0);
		signal E : unsigned (3 downto 0);
		signal F : unsigned (3 downto 0);
		signal G : unsigned (3 downto 0);
		
		Signal outA : std_logic;
		Signal outB : std_logic;
		Signal outC : std_logic;
		Signal outD : std_logic;
		Signal outE : std_logic;
		
		Signal BCD_out : unsigned (7 downto 0);
	
		
BEGIN
	
	BCD_out (7) <= '0';
	

	A <= '0' & unsigned(BCD_in(5 downto 3));
	
	
	
	obj1 : entity work.Over4 port map ( Four_in => std_LOGIC_vector(A(6 downto 3)) , Four_out => outA );
	
	B <= unsigned(A) + "0011" When outA = '1' Else unsigned(A) When outA = '0';
	
	BCD_out(6) <= (B(3));
	
	C <= B(2 downto 0) & BCD_in(2);
	
	
	
	obj2 : entity work.Over4 port map ( Four_in => std_logic_vector(C), Four_out =>	outC );
	
	D <= C + "0011" When outC = '1' Else C When outC = '0';
	
	BCD_out(5) <= D(3);
	
	E <= D(2 downto 0) & BCD_in(1);
	
	
	
	obj3 : entity work.Over4 port map ( Four_in => std_logic_vector(E), Four_out => outE );
	
	F <= E + "0011" When outE = '1' Else E When outE = '0';
	
	BCD_out(4 downto 1) <= (F);
	
	
	
	
	BCD_out (0) <= BCD_in(0);
	
	Bout <= std_LOGIC_vector(BCD_out);
	
	
	
END ARCHITECTURE Behaviour;




