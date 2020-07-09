library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity debounce is
  port(
    clk     : in  std_logic;  --input clock
    button  : in  std_logic;  --input signal
    result  : out std_logic); --debounced signal
end debounce;

architecture Behaviour of debounce is
  
  signal flipflopA,  flipflopB  : std_logic; --input flip flop
  
  signal counter_reset : std_logic; --sync reset to zero
 
  signal counter_out : std_logic_vector(19 downto 0) := (others => '0'); --counter output
  
begin

  counter_reset <= flipflopA XOR flipflopB; -- determine when to start counter
  
  process(clk)
  begin

   if rising_edge(clk)then
	
     flipflopA <= button;
     
	  flipflopB <= flipflopA;
     
	  if(counter_reset = '1') then  --reset counter 
      
		counter_out <= (others => '0');
     
	  elsif(counter_out(19) = '0') then --stable input not
      
		counter_out <= counter_out + 1;
     
	  else                                        --stable input
       
		 result <= flipflopB;
     
	  end if;  
		
   end if;
  end process;
end Behaviour;
