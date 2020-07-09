LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY PreScale26 IS
PORT (
		clk_in_pre : in std_logic;
		count_enb : in std_logic;
		Aclear : in std_logic;
		
		clk_out : out std_LOGIC
);
END ENTITY PreScale26;

ARCHITECTURE Behaviour OF PreScale26 IS

	Signal Y : std_logic_vector (25 downto 0);
	Signal Z : std_logic_vector (25 downto 0);

	Signal zero : std_logic_vector (25 downto 0);
	
	Signal D : std_logic;
	Signal Aa : std_logic_vector (25 downto 0);
	Signal Ba : std_logic_vector (25 downto 0);
	
	Signal MuxOut : std_logic_vector (25 downto 0);
	Signal ChanSel : std_logic;
	Signal C_OR_AC : std_logic;
	
Begin
		
		zero <= (others => '0');
		
		Y <= MuxOut when rising_edge(clk_in_pre);
		
		MuxOut <= Ba when Aclear = '0' else zero;
		
		
		Incrementer:	Entity work.Inc26 port map ( input => Y, output => Aa );
		
		
		Ba <= Aa When (count_enb = '1') Else Y When (count_enb = '0');
		
		
		clk_out <= Y(25); 
	
	
END Behaviour;
