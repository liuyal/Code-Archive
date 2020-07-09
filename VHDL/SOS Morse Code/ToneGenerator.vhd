Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity ToneGenerator is
	Port (
			clear : in std_logic;
			Freq : in unsigned (15 downto 0);
			clk : in std_logic;
			WaveOut : out signed (15 downto 0)
	);
End Entity ToneGenerator;


Architecture COND of ToneGenerator is
	
	Signal Freq22 : signed (21 downto 0);
	
	Signal zero : signed (21 downto 0);
	Signal one : signed (21 downto 2);
	Signal one22 : signed (21 downto 0);
	
	Signal Mux_out,A,Y : signed (21 downto 0):= (others => '0');
	

Begin

	zero <= (others => '0');
	
	Freq22 <=  "000000" & signed(Freq) ;

	A <= Y + Freq22;
	
	Mux_out <= A when clear = '1' else zero;
	
	Y <= Mux_out when rising_edge(clk);
	
	WaveOut <= Y (15 downto 0);



End COND;