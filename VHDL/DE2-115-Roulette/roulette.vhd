LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
 
LIBRARY WORK;
USE WORK.ALL;

----------------------------------------------------------------------
--
--  This is the top level template for Lab 2.  Use the schematic on Page 4
--  of the lab handout to guide you in creating this structural description.
--  The combinational blocks have already been designed in previous tasks,
--  and the spinwheel block is given to you.  Your task is to combine these
--  blocks, as well as add the various registers shown on the schemetic, and
--  wire them up properly.  The result will be a roulette game you can play
--  on your DE2.
--
-----------------------------------------------------------------------

ENTITY roulette IS
	PORT(   
		CLOCK_50 : IN STD_LOGIC; -- the fast clock for spinning wheel
		KEY : IN STD_LOGIC_VECTOR(3 downto 0);  -- includes slow_clock and reset
		SW : IN STD_LOGIC_VECTOR(17 downto 0);
		LEDG : OUT STD_LOGIC_VECTOR(3 DOWNTO 0);  -- ledg
		LEDR : OUT STD_LOGIC_VECTOR(17 downto 0); -- ledr
		
		HEX7 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);  -- digit 7
		HEX6 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);  -- digit 6
		HEX5 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);  -- digit 5
		HEX4 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);  -- digit 4
		HEX3 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);  -- digit 3
		HEX2 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);  -- digit 2
		HEX1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);  -- digit 1
		HEX0 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)   -- digit 0
	);
END roulette;


ARCHITECTURE structural OF roulette IS
		
		signal dbButton : std_LOGIC_VECTOR (3 downto 0);
		Signal reset,slow_clock : std_LOGIC;
		
		Signal spin_result_out, spin_result_latched : UNSIGNED(5 downto 0);
		
		signal bet1_value : unsigned (5 downto 0);
		signal bet2_colour : std_LOGIC;
		signal bet3_dozen : unsigned (1 downto 0);
		
		signal bet1_wins, bet2_wins, bet3_wins : std_LOGIC;
		
		signal bet1_amount, bet2_amount, bet3_amount : unsigned (2 downto 0);
		
		signal money, new_money : unsigned (11 downto 0) := (others => '0');
		
		signal money_display : std_LOGIC_VECTOR (15 downto 0);
		
		Signal BCD6_out,BCD6_out2 : std_LOGIC_VECTOR(7 downto 0);
		signal TOHex7, TOHex6, TOHex5, TOHex4, TOHex3, TOHex2, TOHex1, TOHex0  : std_LOGIC_VECTOR(6 downto 0);

BEGIN

	reset <= dbButton(3);
   slow_clock <= dbButton(2);
	
	LEDR (17 downto 16) <= (others => '1');
	LEDR (12) <= '1';
	LEDR (8 downto 3) <= (others => '1');
	
	LEDG(0) <= bet1_wins;
	LEDG(1) <= bet2_wins;
	LEDG(2) <= bet3_wins;
	
	HEX7 <= TOHex7;
	HEX6 <= TOHex6;
	
	HEX5 <= TOHex5;
	HEX4 <= TOHex4;
	
	HEX3 <= TOHex3;
	HEX2 <= TOHex2;
	HEX1 <= TOHex1;
	HEX0 <= TOHex0;
	
	db3 : Entity work.debounce Port Map (clk => CLOCK_50, button => key(3), result => dbButton(3));
	db2 : Entity work.debounce Port Map (clk => CLOCK_50, button => key(2), result => dbButton(2));
	db1 : Entity work.debounce Port Map (clk => CLOCK_50, button => key(1), result => dbButton(1));
	db0 : Entity work.debounce Port Map (clk => CLOCK_50, button => key(0), result => dbButton(0));
	
   wheel : Entity work.spinwheel port map ( fast_clock => CLOCK_50 , resetb => reset, spin_result => spin_result_out);
 
	BCD6bit1 : Entity work.BCD port map (BCD_in => std_LOGIC_VECTOR(spin_result_latched), Bout => BCD6_out);
	BCD_to7A : Entity work.digit7seg port map (digit => BCD6_out(7 downto 4), seg7 => TOHex7);
   BCD_to7B : Entity work.digit7seg port map (digit => BCD6_out(3 downto 0), seg7 => TOHex6);
	
	BCD6bit2 : Entity work.BCD port map (BCD_in => SW (8 downto 3), Bout => BCD6_out2);
	BCD_to7C : Entity work.digit7seg port map (digit => BCD6_out2(7 downto 4), seg7 => TOHex5);
   BCD_to7D : Entity work.digit7seg port map (digit => BCD6_out2(3 downto 0), seg7 => TOHex4);
 
	Win_detect : Entity work.win port map(spin_result_latched => spin_result_latched, 
													  bet1_value => bet1_value, bet2_colour => bet2_colour, bet3_dozen => bet3_dozen,
													  bet1_wins => bet1_wins, bet2_wins => bet2_wins, bet3_wins => bet3_wins);
			
	Money_Calc : Entity work.new_balance port map (money => money, value1 => bet1_amount, value2 => bet2_amount,  value3 => bet3_amount,
															bet1_wins => bet1_wins, bet2_wins => bet2_wins, bet3_wins => bet3_wins,	new_money => new_money);
	
	BCD12bit :  Entity work.BCD12 port map (BCD_in => std_LOGIC_VECTOR(new_money), Bout => money_display);
	
	BCD_to7E : Entity work.digit7seg port map (digit => money_display(15 downto 12), seg7 => TOHex3);
   BCD_to7F : Entity work.digit7seg port map (digit => money_display(11 downto 8), seg7 => TOHex2);
	BCD_to7G : Entity work.digit7seg port map (digit => money_display(7 downto 4), seg7 => TOHex1);
   BCD_to7H : Entity work.digit7seg port map (digit => money_display(3 downto 0), seg7 => TOHex0);
	
	process(all)
	begin
 
	if reset = '0' then
	
		spin_result_latched <= (others => '0');
		
		bet1_value <= (others => '0');
		bet2_colour <= '0';
		bet3_dozen <= (others => '0');
		
		bet1_amount <= (others => '0');
		bet2_amount <= (others => '0');
		bet3_amount <= (others => '0');
		
		money <= to_unsigned(32, money'length);
		
	elsif rising_edge(slow_clock) then
	
		spin_result_latched <= spin_result_out;
		
		bet1_value <= unsigned(SW(8 downto 3));
		bet2_colour <= SW(12);
		bet3_dozen <= unsigned(SW (17 downto 16));
		
		bet1_amount <= unsigned(SW(2 downto 0));
		bet2_amount <= unsigned(SW(11 downto 9));
		bet3_amount <= unsigned(SW(15 downto 13));
		
		money <= new_money;
		
	end if;

	end process;
 
END;
