LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY Top IS
PORT (
	KEY : in std_LOGIC_vector (1 downto 1);
	SW : in std_LOGIC_vector (1 downto 0);
	HEX0, HEX1 : out std_LOGIC_vector (6 downto 0)
);
END ENTITY Top;

ARCHITECTURE Behaviour OF Top IS

SIGNAL WireA : std_LOGIC_vector(7 downto 0);

signal A :  std_LOGIC_vector(5 downto 0);


BEGIN 
		
		
		count : ENTITY work.Fcount Port Map(clk=>KEY(1),Q => A ,count_enb => SW(1),Aclear => SW(0));	

		
		BCD_con : EntITY work.BCD port Map (BCD_in => A, Bout => WireA); 
		
		
		hex01: ENTITY work.SegDecoder Port Map (D => WireA (7 downto 4), Y => HEX1 );

		hex00: ENTITY work.SegDecoder Port Map (D => WireA (3 downto 0), Y => HEX0 );
		
		
END Behaviour;

