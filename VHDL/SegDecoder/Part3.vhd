LIBRARY IEEE;
USE ieee.std_logic_1164.all; 


ENTITY Part3 IS 
	PORT
	(  SW : IN std_logic_vector( 17 downto 0 );
		KEY : IN std_LOGIC_vector(3 downto 0);
		HEX0, HEX1 : OUT std_logic_vector( 6 downto 0 ));
END Part3;
 

ARCHITECTURE COND OF Part3 IS


SIGNAL SegDecoder : STD_LOGIC;

SIGNAL Wire : STD_LOGIC_vector(7 downto 0);

BEGIN

	Wire <= SW (7 downto 0)When (KEY(0)= '1') ELSE SW(17 downto 10);



	SEG1:	ENTITY WORK.SegDecoder PORT MAP 
	( D(3 downto 0) => Wire (3 downto 0),Y(6 downto 0)=> HEX0 (6 downto 0));


	
	
	
	SEG2:	ENTITY WORK.SegDecoder PORT MAP 
	( D(3 downto 0) => Wire (7 downto 4),Y(6 downto 0)=> HEX1 (6 downto 0));

	
END COND;










