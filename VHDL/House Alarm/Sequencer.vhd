Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity Sequencer is
	Port (
			ENB : in std_logic;
			clk_Seq : in std_logic;
			Q : out std_logic_vector (10 downto 0)
	);
End Entity Sequencer ;


Architecture COND of Sequencer is

	constant Hundred : unsigned := "10000000000";
	constant zero : unsigned := "00000000000";
	Signal Y : unsigned (10 downto 0):= "00000000000";
	Signal one : unsigned(10 downto 0) := "00000000001";
	Signal A,B,C : unsigned (10 downto 0);

Begin

	Y <= B when rising_edge(clk_Seq);
	
	C <=  Y - one;
	
	A <= zero when Y = zero else C;
	
	B <= A when (ENB = '0') Else Hundred when ENB = '1';
	
	
	Q <= std_logic_vector(Y);
	
	
End COND;










