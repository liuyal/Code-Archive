LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
 
ENTITY TimesTen IS
PORT (

	X : in Std_logic_vector (3 downto 0);
	TenX : out Std_logic_vector (7 downto 0)
	
);
END ENTITY TimesTen;


ARCHITECTURE Behaviour OF TimesTen IS

	Signal wireC: std_logic;
	Signal wireD: std_logic;
	Signal wireE: std_logic;

	
	
BEGIN
	 TenX(0) <= '0';
	 TenX(1) <= X(0);
	 TenX(2) <= X(1);


	obj3: work.FullAdder Port Map( A=>X(0) , B => X(2), C =>'0', Sum => TenX(3), Carry => wireC);

	obj4: work.FullAdder Port Map( A=>X(1) , B => X(3), C =>wireC, Sum => TenX(4), Carry => wireD);

	obj5: work.HalfAdder Port Map( A=>X(2) , B =>wireD, Sum => TenX(5), Carry => wireE);

	obj6: work.HalfAdder Port Map( A=>X(3) , B =>wireE, Sum => TenX(6), Carry => TenX(7));

END Behaviour;











