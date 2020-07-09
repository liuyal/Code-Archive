Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity MorseGenerator is
	Port (
			Morse_clk : in std_logic;
			PulseOut : out std_logic;
			Pulse_6 : out unsigned (5 downto 0)
			
	);
End Entity MorseGenerator;


Architecture COND of MorseGenerator is
	
	Signal SlowClock : std_logic;
	Signal Pulse_wire : unsigned (5 downto 0);
	
	Signal SOS_Pulse : std_logic;
	
Begin

	--1010100011101110111000101010000000
	
	PreScaler : Entity work.PreScale Port Map(
	clk_in_pre => Morse_clk, clk_out => SlowClock, count_enb => '1', Aclear => '0');
	
	
	Seq : Entity work.Sequencer Port Map( clk_Seq => SlowClock, Q => Pulse_wire);
	
	
	With Pulse_wire Select SOS_Pulse <=
	
			'1' When "100001", -- 33
			'1' When "011111", -- 31
			'1' When "011101", -- 29
		
			'1' When "011001", -- 25
			'1' When "011000", -- 24
			'1' When "010111", -- 23
	
			'1' When "010101", -- 21
			'1' When "010100", -- 20
			'1' When "010011", -- 19
	
			'1' When "010001", -- 17
			'1' When "010000", -- 16
			'1' When "001111", -- 15
	
			'1' When "001011", -- 11
			'1' When "001001", -- 9
			'1' When "000111", -- 7
			'0' When Others;
	
	Pulse_6 <= Pulse_wire;
	
	
	PulseOut <= SOS_Pulse;
	
End COND;