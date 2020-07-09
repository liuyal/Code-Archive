LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL; 

ENTITY TestTimesTen IS
PORT (

	SW : in Std_logic_vector (3 downto 0);
	HEX0, HEX1, HEX2, HEX3 : out Std_logic_vector (6 downto 0)
	
);
END ENTITY TestTimesTen;




ARCHITECTURE Behaviour OF TestTimesTen IS

SIGNAL WireA : STD_LOGIC_vector(7 downto 0);
SIGNAL WireB : STD_LOGIC_vector(7 downto 0);
SIGNAL WireC : STD_LOGIC_vector(7 downto 0);
SIGNAL WireD : STD_LOGIC_vector(7 downto 0);

BEGIN

		obj1: work.TimesTen Port Map( X => SW,  TenX => WireA (7 downto 0));
		hex01: work.SegDecoder Port Map (D => WireA (7 downto 4), Y => Hex3 );
		
		obj2: work.TimesTen Port Map( X => WireA (3 downto 0),  TenX => WireB (7 downto 0));
		hex02: work.SegDecoder Port Map (D => WireB (7 downto 4), Y => Hex2 );
		
		obj3: work.TimesTen Port Map( X => WireB (3 downto 0),  TenX => WireC (7 downto 0));
		hex03: work.SegDecoder Port Map (D => WireC (7 downto 4), Y => Hex1 );
		
		
		obj4: work.TimesTen Port Map( X => WireC (3 downto 0),  TenX => WireD (7 downto 0));
		hex04: work.SegDecoder Port Map (D => WireD (7 downto 4), Y => Hex0 );
		
		
		

END Behaviour;
