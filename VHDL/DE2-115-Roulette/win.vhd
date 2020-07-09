LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
 
LIBRARY WORK;
USE WORK.ALL;

--------------------------------------------------------------
--
--  This is a skeleton you can use for the win subblock.  This block determines
--  whether each of the 3 bets is a winner.  As described in the lab
--  handout, the first bet is a "straight-up" bet, teh second bet is 
--  a colour bet, and the third bet is a "dozen" bet.
--
--  This should be a purely combinational block.  There is no clock.
--  Remember the rules associated with Pattern 1 in the lectures.
--
---------------------------------------------------------------

ENTITY win IS
	PORT(
	          spin_result_latched : in unsigned(5 downto 0);  -- result of the spin (the winning number)
             bet1_value : in unsigned(5 downto 0); -- value for bet 1
             bet2_colour : in std_logic;  -- colour for bet 2
             bet3_dozen : in unsigned(1 downto 0);  -- dozen for bet 3
             bet1_wins : out std_logic;  -- whether bet 1 is a winner
             bet2_wins : out std_logic;  -- whether bet 2 is a winner
             bet3_wins : out std_logic); -- whether bet 3 is a winner
END win;


ARCHITECTURE behavioural OF win IS

BEGIN
		--process(spin_result_latched, bet1_value, bet2_colour, bet3_dozen)
		process(all)
			variable number : unsigned (5 downto 0);
			variable color : std_logic;
			variable ranges : unsigned (1 downto 0);			
		
		begin
		
		number := spin_result_latched;
		
			if ((number >= 1) and (number <= 10)) or ((number >= 19) and (number <= 28)) then --[1,10] [19,28]
			
				if (number(0)) = '0' then
					color := '0'; -- even
				else
					color := '1'; -- odd
				end if;
				
			elsif ((number >= 11) and (number <= 18)) or ((number >= 29) and (number <= 36)) then --[11,18] [29,36]
				
				if number(0) = '0' then
					color := '1'; -- even
				else
					color := '0'; -- odd
				end if;
			else
					color := not bet2_colour;	
			end if;

			if (number >= 1) and (number <= 12) then --[1,12]			
				ranges := "00";
			elsif (number >= 13) and (number <= 24) then --[13,24]
				ranges := "01";
			elsif (number >= 25) and (number <= 36) then --[25,36]
				ranges := "10";
			else
				ranges := "11";
			end if;
			

			if number = bet1_value then
				bet1_wins <= '1';
			else
				bet1_wins <= '0';
			end if;

			if color = bet2_colour then
				bet2_wins <= '1';
			else
				bet2_wins <= '0';
			end if;

			if ranges = bet3_dozen then
				bet3_wins <= '1';
			else
				bet3_wins <= '0';
			end if;
		end process;
END;