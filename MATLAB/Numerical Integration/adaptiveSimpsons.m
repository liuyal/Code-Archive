
function [estIntegral, intervals] = adaptiveSimpsons(f, a, b, tol, s)

c = ((a+b)/2);

x = integralSimpsons (f,a,c);
y = integralSimpsons (f,c,b);

R = abs(s - x - y);

    if R < 15*tol 
      corr = (1/15)*(x+y-s);
      estIntegral = x + y + corr; 
      intervals = [a,c;c,b];
  
       return
    else
        
        [Left_sub, interval_1]= adaptiveSimpsons(f, a, c, tol/2, x);
        [Right_sub, interval_2]= adaptiveSimpsons(f, c, b, tol/2, y);
        
        estIntegral = Left_sub + Right_sub;
        
        intervals = vertcat (interval_1, interval_2 );
    
       return
    end

end











