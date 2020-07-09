%Test for every 2 hand card combinations

Rank = {'A','K','Q','J','10','9','8','7','6','5','4','3','2'};
Suits = {'S','D','H','C'};

count = 0;
card = {0};

%Creates Deck of 52 Cards
for i = Suits;
    for ii = Rank
        for iii = 1:13
            count = count + 1;
            t = [ii i];
            card{count} = cell2mat(t);
        break
        end
    end
end

card = card';
cardCombo = nchoosek(card,2);

%Every loop puts card into card1 & card2
for i = 1:length(cardCombo)

    card1 = cardCombo(i,1);
    card2 = cardCombo(i,2);
    
    card1 = cell2mat(card1);
    card2 = cell2mat(card2);

    CardMatrix = Texas_HoldEm(card1,card2); %BreakPoint here
    
    ShowCard = [card1,' ',card2];
    disp(ShowCard)
end

