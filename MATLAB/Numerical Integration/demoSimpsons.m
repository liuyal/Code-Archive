%Simpons Integral

clear all
close all

fun = @f;

Low = 1;
Up = 9;
tol = 1e-2;

estIntegral = integralSimpsons (fun,Low,Up);
[estIntegral, intervals] = adaptiveSimpsons(fun, Low, Up, tol, estIntegral);

x = linspace(0,10,1000);
p = plot(x,f(x));
title('Adaptive Simpsons');

hold on

ax = gca;
ylimits = get(ax,'YLim');

I = intervals;
I(:,1) = I(:,2);
h = line(I,ylimits);
set(h,'LineStyle',':','Color','k');

hold off

















