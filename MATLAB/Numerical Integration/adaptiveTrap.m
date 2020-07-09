
function [estIntegral, intervals] = adaptiveTrap(f, a, b, tol, s)

c = ((a+b)/2);

x = integralTrap (f,a,c);
y = integralTrap (f,c,b);

R = abs(s - x - y);

    if R < 7*tol 
      corr = (1/7)*(x+y-s);
      estIntegral = x + y + corr; 
      intervals = [a,c;c,b];
  
       return
    else
        
        [Left_sub, interval_1]= adaptiveTrap(f, a, c, tol/2, x);
        [Right_sub, interval_2]= adaptiveTrap(f, c, b, tol/2, y);
        
        estIntegral = Left_sub + Right_sub;
        
        intervals = vertcat (interval_1, interval_2 );
    
       return
    end

end











