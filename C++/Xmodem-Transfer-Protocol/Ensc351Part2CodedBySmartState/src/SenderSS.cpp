
#pragma warning(disable: 4786)
#pragma warning(disable: 4290)

//Additional Includes
#include <iostream>
#include <stdlib.h>

#include "SenderSS.h"
#include "SenderX.h"

/*Messages
Define user specific messages in a file and
include that file in the additional includes section in 
the model.
-- FOLLOWING MESSAGES ARE USED --
SER
*/

//Additional Declarations
#define c wParam

namespace Sender_SS
{
using namespace std;
using namespace smartstate;

//State Mgr
//--------------------------------------------------------------------
SenderSS::SenderSS(SenderX* ctx, bool startMachine/*=true*/)
 : StateMgr("SenderSS"),
   myCtx(ctx)
{
	myConcStateList.push_back(new Sender_TopLevel_SenderSS("Sender_TopLevel_SenderSS", 0, this));

	if(startMachine)
		start();
}

SenderX& SenderSS::getCtx() const
{
	return *myCtx;
}

//Base State
//--------------------------------------------------------------------
SenderBaseState::SenderBaseState(const string& name, BaseState* parent, SenderSS* mgr)
 : BaseState(name, parent, mgr)
{
}

//--------------------------------------------------------------------
Sender_TopLevel_SenderSS::Sender_TopLevel_SenderSS(const string& name, BaseState* parent, SenderSS* mgr)
 : SenderBaseState(name, parent, mgr)
{
	myHistory = false;
	mySubStates.push_back(new START_Sender_TopLevel("START_Sender_TopLevel", this, mgr));
	mySubStates.push_back(new ACKNAK_Sender_TopLevel("ACKNAK_Sender_TopLevel", this, mgr));
	mySubStates.push_back(new EOT1_Sender_TopLevel("EOT1_Sender_TopLevel", this, mgr));
	mySubStates.push_back(new EOTEOT_Sender_TopLevel("EOTEOT_Sender_TopLevel", this, mgr));
	mySubStates.push_back(new CAN_Sender_TopLevel("CAN_Sender_TopLevel", this, mgr));
	setType(eSuper);
}

void Sender_TopLevel_SenderSS::onEntry()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("> Sender_TopLevel_SenderSS <onEntry>");

	SenderX& ctx = getMgr()->getCtx();

	// Code from Model here
	ctx.Crcflg=true; ctx.prep1stBlk(); ctx.errCnt=0; 
	ctx.firstCrcBlk=true;
}

void Sender_TopLevel_SenderSS::onExit()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("< Sender_TopLevel_SenderSS <onExit>");

}

void Sender_TopLevel_SenderSS::onMessage(const Mesg& mesg)
{
	if(mesg.message == SER)
		onSERMessage(mesg);
	else 
		super::onMessage(mesg);
}

void Sender_TopLevel_SenderSS::onSERMessage(const Mesg& mesg)
{
	int wParam = mesg.wParam;
	int lParam = mesg.lParam;
	SenderX& ctx = getMgr()->getCtx();

		/* -g option specified while compilation. */
		myMgr->debugLog("Sender_TopLevel_SenderSS SER <message trapped>");

	if(true)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("Sender_TopLevel_SenderSS SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("Sender_TopLevel_SenderSS", "FinalState");
		/* -g option specified while compilation. */
		myMgr->debugLog("Sender_TopLevel_SenderSS SER <executing effect>");


		//User specified effect begin
		cerr << "Sender received totally unexpected char #" << c << ": " << (char) c << endl;
		exit(EXIT_FAILURE);
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("Sender_TopLevel_SenderSS SER <executing entry>");

		getMgr()->executeEntry(root, "FinalState");
		return;
	}

	super::onMessage(mesg);
}

//--------------------------------------------------------------------
ACKNAK_Sender_TopLevel::ACKNAK_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr)
 : SenderBaseState(name, parent, mgr)
{
	myHistory = false;
}

void ACKNAK_Sender_TopLevel::onEntry()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("> ACKNAK_Sender_TopLevel <onEntry>");

}

void ACKNAK_Sender_TopLevel::onExit()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("< ACKNAK_Sender_TopLevel <onExit>");

}

void ACKNAK_Sender_TopLevel::onMessage(const Mesg& mesg)
{
	if(mesg.message == SER)
		onSERMessage(mesg);
	else 
		super::onMessage(mesg);
}

void ACKNAK_Sender_TopLevel::onSERMessage(const Mesg& mesg)
{
	int wParam = mesg.wParam;
	int lParam = mesg.lParam;
	SenderX& ctx = getMgr()->getCtx();

		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <message trapped>");

	if((c==NAK ||                (c=='C' && ctx.firstCrcBlk)) && (ctx.errCnt < errB) )
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.resendBlk();
		ctx.errCnt++;
		//User specified effect end

		return;
	}
	else
	if(c==NAK && (ctx.errCnt >= errB))
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("ACKNAK_Sender_TopLevel", "FinalState");
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.can8();
		ctx.result="ExcessiveNAKs";
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "FinalState");
		return;
	}
	else
	if((c==ACK) && !ctx.bytesRd)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("ACKNAK_Sender_TopLevel", "EOT1_Sender_TopLevel");
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.sendByte(EOT);ctx.errCnt=0; ctx.firstCrcBlk=false;
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "EOT1_Sender_TopLevel");
		return;
	}
	else
	if((c==ACK) && ctx.bytesRd)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.sendBlkPrepNext(); 
		ctx.errCnt=0; 
		ctx.firstCrcBlk=false;
		//User specified effect end

		return;
	}
	else
	if(c == CAN)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("ACKNAK_Sender_TopLevel", "CAN_Sender_TopLevel");
		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		//nil
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("ACKNAK_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "CAN_Sender_TopLevel");
		return;
	}

	super::onMessage(mesg);
}

//--------------------------------------------------------------------
EOT1_Sender_TopLevel::EOT1_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr)
 : SenderBaseState(name, parent, mgr)
{
	myHistory = false;
}

void EOT1_Sender_TopLevel::onEntry()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("> EOT1_Sender_TopLevel <onEntry>");

	SenderX& ctx = getMgr()->getCtx();

	// Code from Model here
	/*ctx.sendByte(
	EOT)*/
}

void EOT1_Sender_TopLevel::onExit()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("< EOT1_Sender_TopLevel <onExit>");

}

void EOT1_Sender_TopLevel::onMessage(const Mesg& mesg)
{
	if(mesg.message == SER)
		onSERMessage(mesg);
	else 
		super::onMessage(mesg);
}

void EOT1_Sender_TopLevel::onSERMessage(const Mesg& mesg)
{
	int wParam = mesg.wParam;
	int lParam = mesg.lParam;
	SenderX& ctx = getMgr()->getCtx();

		/* -g option specified while compilation. */
		myMgr->debugLog("EOT1_Sender_TopLevel SER <message trapped>");

	if(c == ACK)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("EOT1_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("EOT1_Sender_TopLevel", "FinalState");
		/* -g option specified while compilation. */
		myMgr->debugLog("EOT1_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.result="1st EOT ACK'd";
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("EOT1_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "FinalState");
		return;
	}
	else
	if(c==NAK)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("EOT1_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("EOT1_Sender_TopLevel", "EOTEOT_Sender_TopLevel");
		/* -g option specified while compilation. */
		myMgr->debugLog("EOT1_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.sendByte(EOT);
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("EOT1_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "EOTEOT_Sender_TopLevel");
		return;
	}

	super::onMessage(mesg);
}

//--------------------------------------------------------------------
START_Sender_TopLevel::START_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr)
 : SenderBaseState(name, parent, mgr)
{
	myHistory = false;
}

void START_Sender_TopLevel::onEntry()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("> START_Sender_TopLevel <onEntry>");

}

void START_Sender_TopLevel::onExit()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("< START_Sender_TopLevel <onExit>");

}

void START_Sender_TopLevel::onMessage(const Mesg& mesg)
{
	if(mesg.message == SER)
		onSERMessage(mesg);
	else 
		super::onMessage(mesg);
}

void START_Sender_TopLevel::onSERMessage(const Mesg& mesg)
{
	int wParam = mesg.wParam;
	int lParam = mesg.lParam;
	SenderX& ctx = getMgr()->getCtx();

		/* -g option specified while compilation. */
		myMgr->debugLog("START_Sender_TopLevel SER <message trapped>");

	if(((c == NAK) || (c == 'C')) && !ctx.bytesRd)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("START_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("START_Sender_TopLevel", "EOT1_Sender_TopLevel");
		/* -g option specified while compilation. */
		myMgr->debugLog("START_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		if (c==NAK) {ctx.firstCrcBlk=false;}
		ctx.sendByte(EOT);
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("START_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "EOT1_Sender_TopLevel");
		return;
	}
	else
	if((c==NAK || c=='C') && ctx.bytesRd)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("START_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("START_Sender_TopLevel", "ACKNAK_Sender_TopLevel");
		/* -g option specified while compilation. */
		myMgr->debugLog("START_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		if (c==NAK) {ctx.Crcflg=false; 
		   ctx.cs1stBlk();
		   ctx.firstCrcBlk=false;}
		ctx.sendBlkPrepNext();
		
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("START_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "ACKNAK_Sender_TopLevel");
		return;
	}

	super::onMessage(mesg);
}

//--------------------------------------------------------------------
EOTEOT_Sender_TopLevel::EOTEOT_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr)
 : SenderBaseState(name, parent, mgr)
{
	myHistory = false;
}

void EOTEOT_Sender_TopLevel::onEntry()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("> EOTEOT_Sender_TopLevel <onEntry>");

}

void EOTEOT_Sender_TopLevel::onExit()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("< EOTEOT_Sender_TopLevel <onExit>");

}

void EOTEOT_Sender_TopLevel::onMessage(const Mesg& mesg)
{
	if(mesg.message == SER)
		onSERMessage(mesg);
	else 
		super::onMessage(mesg);
}

void EOTEOT_Sender_TopLevel::onSERMessage(const Mesg& mesg)
{
	int wParam = mesg.wParam;
	int lParam = mesg.lParam;
	SenderX& ctx = getMgr()->getCtx();

		/* -g option specified while compilation. */
		myMgr->debugLog("EOTEOT_Sender_TopLevel SER <message trapped>");

	if(c==NAK)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("EOTEOT_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.sendByte(EOT);
		//User specified effect end

		return;
	}
	else
	if(c==ACK)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("EOTEOT_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("EOTEOT_Sender_TopLevel", "FinalState");
		/* -g option specified while compilation. */
		myMgr->debugLog("EOTEOT_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.result="Done";
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("EOTEOT_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "FinalState");
		return;
	}

	super::onMessage(mesg);
}

//--------------------------------------------------------------------
CAN_Sender_TopLevel::CAN_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr)
 : SenderBaseState(name, parent, mgr)
{
	myHistory = false;
}

void CAN_Sender_TopLevel::onEntry()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("> CAN_Sender_TopLevel <onEntry>");

}

void CAN_Sender_TopLevel::onExit()
{
	/* -g option specified while compilation. */
	myMgr->debugLog("< CAN_Sender_TopLevel <onExit>");

}

void CAN_Sender_TopLevel::onMessage(const Mesg& mesg)
{
	if(mesg.message == SER)
		onSERMessage(mesg);
	else 
		super::onMessage(mesg);
}

void CAN_Sender_TopLevel::onSERMessage(const Mesg& mesg)
{
	int wParam = mesg.wParam;
	int lParam = mesg.lParam;
	SenderX& ctx = getMgr()->getCtx();

		/* -g option specified while compilation. */
		myMgr->debugLog("CAN_Sender_TopLevel SER <message trapped>");

	if(c == CAN)
	{
		/* -g option specified while compilation. */
		myMgr->debugLog("CAN_Sender_TopLevel SER <executing exit>");

		const BaseState* root = getMgr()->executeExit("CAN_Sender_TopLevel", "FinalState");
		/* -g option specified while compilation. */
		myMgr->debugLog("CAN_Sender_TopLevel SER <executing effect>");


		//User specified effect begin
		ctx.result=
		     "RcvCancelled";
		/*ctx.clearCan()*/
		//User specified effect end

		/* -g option specified while compilation. */
		myMgr->debugLog("CAN_Sender_TopLevel SER <executing entry>");

		getMgr()->executeEntry(root, "FinalState");
		return;
	}

	super::onMessage(mesg);
}


} /*end namespace*/

//___________________________________vv^^vv___________________________________
