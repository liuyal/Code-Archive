LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY TestBCDCount2 IS
PORT (
	KEY : in std_LOGIC_vector (3 downto 0);
   SW : in std_Logic_vector (7 downto 0);
	LEDR: out std_LOGIC_vector (7 downto 0)
		
);

END ENTITY TestBCDCount2;


ARCHITECTURE Behaviour OF TestBCDCount2 IS



Begin


Oni : Entity work.BCDCount2 Port Map( Clock => KEY(0), Clear => SW(1), 
Enable => SW(0), BCD1 => LEDR (7 downto 4),BCD0 => LEDR (3 downto 0));



END Behaviour;