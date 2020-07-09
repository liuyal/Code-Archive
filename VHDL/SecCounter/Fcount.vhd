LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY Fcount IS
PORT (
		--D : in unsigned (3 downto 0);
		clk : in std_logic;
		count_enb : in std_logic;
		Aclear : in std_logic;
		Q : out std_LOGIC_vector(5 downto 0)
);
END ENTITY Fcount;

ARCHITECTURE Behaviour OF Fcount IS

	Signal Y : std_logic_vector (5 downto 0);
	Signal Z : std_logic_vector (5 downto 0);
	
	Signal zero : std_logic_vector (5 downto 0);
	
	Signal D : std_logic;
	Signal Aa : std_logic_vector (5 downto 0);
	Signal Ba : std_logic_vector (5 downto 0);
	Signal Ca : std_LOGIC_vector (5 downto 0);
	
	Signal MuxOut : std_logic_vector (5 downto 0);
	Signal ChanSel : std_logic;
	Signal C_OR_AC : std_logic;
	
	
	
Begin
		
		zero <= "000000";
		
		
		--When (count_enb = '0') Else '0' When (count_enb = '1');
		
		Y <= MuxOut when rising_edge(clk);
		
		MuxOut <= Ba when C_OR_AC = '0' else zero;
		
		C_OR_AC <= ChanSel OR Aclear;
		
		
		
		Incrementer:	Entity work.Inc6 port map ( input => Y, output => Aa );
		
		Ba <= Aa When (count_enb = '1') Else Y When (count_enb = '0');
		--Ca <= Aa When (count_enb = '1') Else zero When (count_enb = '0');
		
		LimitTest:	Entity work.Over60 port map ( A => Ba, Z => ChanSel );
		
		Q <= std_LOGIC_vector(Y); --When Aclear = '0' Else "000000" When Aclear = '1';
	
	
END Behaviour;




