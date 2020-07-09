LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY System_Test IS

PORT (
		CLOCK_50 : in std_logic;
		SW : in  std_logic_vector (17 downto 0);
		KEY : in  std_logic_vector (3 downto 0);
		
		LEDR : out std_logic_vector (17 downto 0);
		LEDG : out std_logic_vector (8 downto 0);
		HEX2 , HEX1, HEX0 : out std_logic_vector (6 downto 0)

);
END ENTITY System_Test;

ARCHITECTURE Cond OF System_Test IS
	
	Signal A,B,C : std_logic;
	Signal Slow_clk : std_logic;
	Signal Alarm_ENB : std_logic;
	Signal Delay_wire : std_logic;
	Signal ARM_ENB : std_logic;
	
	Signal Alarm_clk : std_logic;
	
Begin 


	PreClk1 : Entity work.PreScale port map ( clk_in_pre => CLOCK_50, count_enb => '1', Aclear => '0', clk_out => Slow_clk );
	
	
	Pre_Alarm_Clk : Entity work.PreScale26 port map ( clk_in_pre => CLOCK_50, count_enb => '1', Aclear => '0', clk_out => Alarm_clk );
	

	
	Alarm_BOX :	Entity work.Alarm port map (Enable => Alarm_ENB, Alarm_Clk => Alarm_Clk,
														Seg2 => HEX2, Seg1 => HEX1, Seg0 =>  HEX0);												
												
												
												
	--TestB :	Entity work.System(Basic) port map (ARM=> KEY(3), Clock=>Slow_clk, Doors=>SW (3 downto 0), Hold_out=>LEDG(2),
	--												Ready=>LEDG(8), SysArmed=>LEDG(0), AlarmOn=>Alarm_ENB);				
	
	
	TestD :	Entity work.System(Delays) port map (ARM=> KEY(3), ARM2 => KEY(2), Clock => Slow_clk, Doors => SW(3 downto 0),
				Ready => LEDG(8), SysArmed => LEDG(0), AlarmOn => Alarm_ENB, Hold_out=>LEDG(2),Delay_Signal_out => Delay_wire,
				Delay_arm_out => LEDR(16), ARM2_ENB => ARM_ENB);
		
	
	JB_007 : Entity work.JamesBond port map (Go => KEY(1), Digit => SW(17 downto 15), 
											S0 => LEDG(7), S1=> LEDG(6), S2=> LEDG(5),
													JB_clk => Slow_clk, GotCode => ARM_ENB);
	
	
												
														
	LEDR(3 downto 0) <= SW (3 downto 0);
	LEDR (17) <= Delay_wire;
	LEDG(4) <= ARM_ENB;
	
End Cond;