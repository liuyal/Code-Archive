function CardMatrix=Texas_HoldEm(card1, card2)
Cards = {'A','K','Q','J','10','9','8','7','6','5','4','3','2'};
Suits = {'S','D','H','C'};
NumSuits = length(Suits);
NumCards = length(Cards);

%Parse Player 1's cards
PlayersCards = zeros(1, 2);
PlayersCards(1) = GetCard(card1);
PlayersCards(2) = GetCard(card2);

if PlayersCards(1) == PlayersCards(2)
    error('Player 1 must be dealt two different cards')
end

%Organize Player 1's cards into a matrix
CardMatrix = zeros(4,13);
CardMatrix(PlayersCards) = 1;

%---------------------- INSERT CODE FOR TASK 1 HERE ----------------------%
numPairs = 0;

X = sum(CardMatrix); 

A = 0;
for i = 1:length(X)

   count = X(i);
   
    if count == 0 %4cards combo
        A = nchoosek(4,2);
    else if count == 1 %3cards combo
        A = nchoosek(3,2);
        else            %2cards combo
         A = nchoosek(2,2);   
        end
    end

   numPairs = numPairs + A;
    
end

probPair = numPairs/nchoosek(50,2);

%-------------------------------------------------------------------------%

%---------------------- INSERT CODE FOR TASK 2 HERE ----------------------%
numAceHigh = 0;

B = 0;
for i = 2:length(X)
    
    countAce = X(i);
    
    if countAce == 0 %4cards combo with Ace
        B = nchoosek(4,1);
    else if countAce == 1 %3cards combo with Ace
        B = nchoosek(3,1); 
        else               %2cards combo with Ace
            B = nchoosek(2,1);
        end
    end
    
numAceHigh = numAceHigh + B;
end

if X(1) == 1
numAceHigh = 3*numAceHigh;
else if X(1) == 2
numAceHigh = 2*numAceHigh;
    else
        numAceHigh = 4*numAceHigh;
    end
end

probAceHigh = numAceHigh/nchoosek(50,2);

%-------------------------------------------------------------------------%

%---------------------- INSERT CODE FOR TASK 3 HERE ----------------------%
numSuited = 0;

Z = sum(CardMatrix,2);

C = 0;
for i = 1:length(Z);
    
    countSuit = Z(i);
    
    if countSuit == 0 %same suit 13 cards in 2
        C = nchoosek(13,2);
    else if countSuit == 1 %same suit 12 cards in 2
        C = nchoosek(12,2);
        else                %same suit 10 cards in 2
            C = nchoosek(11,2);
        end
    end
    
    numSuited = numSuited + C;
    
end

probSuited = numSuited/nchoosek(50,2);
%-------------------------------------------------------------------------%

%---------------------- INSERT CODE FOR TASK 4 HERE ----------------------%
numBetter = 0;

detect = sum(card1(1) == card2(1));

if detect == 1 %P1 has 1 Pair

    I = find(X == 2);
   numBetter = (I-1)*nchoosek(4,2);

else if detect == 0 %P1 has no Pair
        
       for ii = 1:length(X)
           highcard = X(ii);
           if highcard == 1
               break;
           end 
       end
        
       
        v = ii-1;
        
        D = 0;
        numC = 50;
        
        for iii = 1:v 
            numC = numC - 4;
            D = 4*(numC);
        numBetter = numBetter + D;
        end
        
        numBetter = numBetter + numPairs;
    end
end

probBetter = numBetter/nchoosek(50,2);

%-------------------------------------------------------------------------%

%---------------------- INSERT CODE FOR TASK 5 HERE ----------------------%

prob = [probBetter,probSuited,probAceHigh,probPair];

ylabel = {'Better Hand','Suited Hand' ,'Ace High Hand' ,'1 Pair'};

barh(prob);

for ii = 1:length(prob) 
   text(prob(ii)+0.005,ii,sprintf('%.2f%%',prob(ii)*100),'FontSize',12);
end

title('Pre-Flop Probabilities for Player 2','FontSize',15);
xlabel('Probability','Fontsize',15);
set(gca,'YTickLabel',ylabel,'Fontsize',15);

%-------------------------------------------------------------------------%

% Gets the card associated with a card string
function card = GetCard(cardStr)
    if isempty(cardStr)
        card = 0;
    else
        cardNum = find(strcmpi(Cards,cardStr(1:(end-1))));
        suit = find(strcmpi(Suits,cardStr(end)));
        if ((length(cardNum) ~= 1) || (length(suit) ~= 1))
            card = 0;
        else
            card = suit + (cardNum - 1) * NumSuits;
        end
    end
end

end