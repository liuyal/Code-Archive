Use Work.Codec.all;

Library ieee;
Use ieee.std_logic_1164.all;

Entity I2CTxCu is
	port (
		Clk, Go, Sdin : in std_logic;
		Op : out RegOp;
		Busy, Sclk : out std_logic );
End Entity I2CTxCu;


Architecture NestedFSM of I2CTxCu is
	Type MainCode is ( idle, start, Packet0, Packet1, Packet2, stop, Mwait );
	Type PacketCode is ( D7, D6, D5, D4, D3, D2, D1, D0, Ack );
	Type CycleCode is ( C0, C1, C2, C3 );
	
	Attribute syn_encoding : string;
	Attribute syn_encoding of MainCode : type is "compact";
	Attribute syn_encoding of PacketCode : type is "compact";
	Attribute syn_encoding of CycleCode : type is "compact";
	
	Signal MainState, NextMainState : MainCode;
	Signal PacketState, NextPacketState : PacketCode;
	Signal CycleState, NextCycleState : CycleCode;

	Signal EOC, EOP, BadAck : std_logic;
	
	Attribute keep : boolean;
	Attribute keep of BadAck : signal is true;
Begin

MSR:	MainState <= NextMainState when (rising_edge(Clk)) else MainState;
MIFL:	NextMainState <= 
			idle when MainState = idle and Go = '0' else
			Mwait when MainState = Mwait and Go = '1' else
			idle when BadAck = '1' else 

			start when MainState = start and EOC = '0' else
			stop when MainState = stop and EOC = '0' else
			Packet0 when MainState = Packet0 and (EOC = '0' or EOP = '0') else 
			Packet1 when MainState = Packet1 and (EOC = '0' or EOP = '0') else 
			Packet2 when MainState = Packet2 and (EOC = '0' or EOP = '0') else 

			start when MainState = idle and Go = '1' else 
			Packet0 when MainState = start and EOC = '1' else
			Packet1 when MainState = Packet0 and EOC = '1' and EOP = '1' else
			Packet2 when MainState = Packet1 and EOC = '1' and EOP = '1' else

			stop when MainState = Packet2 and EOC = '1' and EOP = '1' else
			Mwait when MainState = stop and EOC = '1' else
			idle when MainState = Mwait and Go = '0' else
			idle;
			
CSR:	CycleState <= NextCycleState when (rising_edge(Clk)) else CycleState;
CIFL:	NextCycleState <= 
			C0 when CycleState = C0 and MainState = idle else
			C0 when CycleState = C0 and MainState = Mwait else
			C0 when CycleState = C1 and MainState = start else
			C0 when CycleState = C2 and MainState = stop else
			C0 when CycleState = C3 and (MainState = Packet0 or MainState = Packet1 or MainState = Packet2) else
			C1 when CycleState = C0 and MainState /= idle else
			C0 when BadAck = '1' else
			C2 when CycleState = C1 and MainState /= start else
			C3 when CycleState = C2 and MainState /= stop else
			C0;
COFL:	EOC <=
			'1' when CycleState = C0 and MainState = Idle else
			'1' when CycleState = C1 and MainState = start else
			'1' when CycleState = C2 and MainState = stop else
			'1' when CycleState = C3 else
			'0';
		BadAck <= '1' when PacketState = ack and CycleState = C1 and Sdin = '1' else '0'; 
			
PSR:	PacketState <= NextPacketState when (rising_edge(Clk)) else PacketState;
PIFL:	NextPacketState <=
			D7 when BadAck = '1' else
			D7 when PacketState = D7 and EOC = '0' else
			D6 when PacketState = D6 and EOC = '0' else
			D5 when PacketState = D5 and EOC = '0' else
			D4 when PacketState = D4 and EOC = '0' else
			D3 when PacketState = D3 and EOC = '0' else
			D2 when PacketState = D2 and EOC = '0' else
			D1 when PacketState = D1 and EOC = '0' else
			D0 when PacketState = D0 and EOC = '0' else
			ack when PacketState = ack and EOC = '0' else
			D7 when PacketState = D7 and
					(MainState = start or MainState = stop or
					 MainState = idle  or MainState = Mwait) else
			D6 when PacketState = D7 and
					(MainState = Packet0 or MainState = Packet1 or MainState = Packet2) else
			D5 when PacketState = D6 and EOC = '1' else
			D4 when PacketState = D5 and EOC = '1' else
			D3 when PacketState = D4 and EOC = '1' else
			D2 when PacketState = D3 and EOC = '1' else
			D1 when PacketState = D2 and EOC = '1' else
			D0 when PacketState = D1 and EOC = '1' else
			ack when PacketState = D0 and EOC = '1' else
			D7;
			
POFL:	EOP <= '1' when PacketState = ack else '0';

		Busy <= '0' when MainState = idle else '1';

		Op <= shift when CycleState = C3 else
				shift when CycleState = C1 and ( MainState = start or MainState = stop ) else
				set when MainState = idle else
				init when CycleState = C0 and MainState = start else
				hold;

		Sclk <= 
			'1' when CycleState = C1 or CycleState = C2 else
			'1' when MainState = start or MainState = idle or mainState = Mwait else
			'0';
End Architecture NestedFSM;


--*********************************************************************************************
-- Back to my original code that I accidently destroyed.
-- Here is a example of how to specify the enumerated coding for a state machine.
--*********************************************************************************************
Architecture SingleFSM of I2CTxCu is
	Type MainCode is ( idle, str0, str1, stp0, stp1,
							 DA6s, DA6h, DA5s, DA5h, DA4s, DA4h, DA3s, DA3h,
							 DA2s, DA2h, DA1s, DA1h, DA0s, DA0h, RWs, RWh, ak0s, ak0h,
							 B15s, B15h, B14s, B14h, B13s, B13h, B12s, B12h,
							 B11s, B11h, B10s, B10h, B09s, B09h, B08s, B08h, ak1s, ak1h,
							 B07s, B07h, B06s, B06h, B05s, B05h, B04s, B04h,
							 B03s, B03h, B02s, B02h, B01s, B01h, B00s, B00h, ak2s, ak2h );
							 
	Attribute syn_encoding : string;
	Attribute syn_encoding of MainCode : type is "johnson";
	
	Signal MainState, NextMainState : MainCode;
	Signal HoldOP : RegOp;
	
Begin
--*********************************************************************************************
-- the state register.
--*********************************************************************************************	
SR:	MainState <= NextMainState when (rising_edge(Clk)) else MainState;
--*********************************************************************************************
-- the input forming logic.
--*********************************************************************************************	
IFL:	NextMainState <= 
			idle when MainState = idle and Go = '1' else
			str0 when MainState = idle and Go = '0' else
			str1 when MainState = str0 else

			DA6s when MainState = str1 else
			DA6h when MainState = DA6s else
			DA5s when MainState = DA6h else
			DA5h when MainState = DA5s else
			DA4s when MainState = DA5h else
			DA4h when MainState = DA4s else
			DA3s when MainState = DA4h else
			DA3h when MainState = DA3s else
			DA2s when MainState = DA3h else
			DA2h when MainState = DA2s else
			DA1s when MainState = DA2h else
			DA1h when MainState = DA1s else
			DA0s when MainState = DA1h else
			DA0h when MainState = DA0s else
			RWs when MainState = DA0h else
			RWh when MainState = RWs else

			ak0s when MainState = RWh else
			ak0h when MainState = ak0s and Sdin = '0' else
			idle when MainState = ak0s and Sdin = '1' else
			
			B15s when MainState = ak0h else
			B15h when MainState = B15s else
			B14s when MainState = B15h else
			B14h when MainState = B14s else
			B13s when MainState = B14h else
			B13h when MainState = B13s else
			B12s when MainState = B13h else
			B12h when MainState = B12s else
			B11s when MainState = B12h else
			B11h when MainState = B11s else
			B10s when MainState = B11h else
			B10h when MainState = B10s else
			B09s when MainState = B10h else
			B09h when MainState = B09s else
			B08s when MainState = B09h else
			B08h when MainState = B08s else

			ak1s when MainState = B08h else
			ak1h when MainState = ak1s and Sdin = '0' else
			idle when MainState = ak1s and Sdin = '1' else
			
			B07s when MainState = ak1h else
			B07h when MainState = B07s else
			B06s when MainState = B07h else
			B06h when MainState = B06s else
			B05s when MainState = B06h else
			B05h when MainState = B05s else
			B04s when MainState = B05h else
			B04h when MainState = B04s else
			B03s when MainState = B04h else
			B03h when MainState = B03s else
			B02s when MainState = B03h else
			B02h when MainState = B02s else
			B01s when MainState = B02h else
			B01h when MainState = B01s else
			B00s when MainState = B01h else
			B00h when MainState = B00s else

			ak2s when MainState = B00h else
			ak2h when MainState = ak2s and Sdin = '0' else
			idle when MainState = ak2s and Sdin = '1' else

			stp0 when MainState = ak2h else
			stp1 when MainState = stp0 else
			idle;
			
			
--*********************************************************************************************
-- the output forming logic.
--*********************************************************************************************	
OFL:
		Busy <= '0' when MainState = idle else '1';

		HoldOp <= 
			set  when MainState = idle else
			init when MainState = str0 else
			shift when MainState = str1 else

			shift when MainState = DA6h or MainState = DA5h or MainState = DA4h or MainState = DA3h  else
			shift when MainState = DA2h or MainState = DA1h or MainState = DA0h or MainState = RWh  else
			shift when MainState = ak0h else
			
			shift when MainState = B15h or MainState = B14h or MainState = B13h or MainState = B12h  else
			shift when MainState = B11h or MainState = B10h or MainState = B09h or MainState = B08h  else
			shift when MainState = ak1h else
			
			shift when MainState = B07h or MainState = B06h or MainState = B05h or MainState = B04h  else
			shift when MainState = B03h or MainState = B02h or MainState = B01h or MainState = B00h  else
			shift when MainState = ak2h else

			shift when MainState = stp1 else
			hold;
			
		Op <= HoldOp;	
		Sclk <= '0' when HoldOp = hold else '1';
		
End Architecture SingleFSM;
