Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity Sequencer is
	Port (
			clk_Seq : in std_logic;
			Q : out unsigned (5 downto 0)
	);
End Entity Sequencer ;


Architecture COND of Sequencer is

	Signal num_33,Y : unsigned(5 downto 0) := "100001";
	Signal one : unsigned(5 downto 0) := "000001";
	
	Signal Mux_out : unsigned (5 downto 0);
	Signal WireA : unsigned (5 downto 0);
	Signal Detect : std_logic;
	

Begin

	Y <= Mux_out when rising_edge(clk_Seq);
	
	WireA <= Y - one;
	
	Detection : entity work.At_Zero Port Map( Six_in => std_logic_vector(Y), Six_out => Detect);
	
	Mux_out <= num_33 when Detect = '1' Else WireA when Detect = '0';
	
	Q <= Y;
	
End COND;