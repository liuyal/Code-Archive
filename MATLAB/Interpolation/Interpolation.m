%% -------------- Task 1 --------------

temp_even = [9.2 9.0 6.8 5.9 7.2 9.2 10.9 10.6 10.3 8.2 8.8 7.5];
temp_odd = [9.6 7.7 6.0 4.3 8.9 10.2 10.6 10.7 8.6 8.0 7.1 7.5];

time_even = [0 2 4 6 8 10 12 14 16 18 20 22];
time_odd = [1 3 5 7 9 11 13 15 17 19 21 23];

time = (0:1:23);

%Actual temp vs time
temp = [temp_even' temp_odd'];
temp = reshape(temp', [24 1]);

%Interpolation
P = polyfit(time_even,temp_even,1);
temp_int_odd = polyval(P,time_odd); %At odd times
MSE_T1 = sum((temp_int_odd - temp_odd).^2)/length(temp_odd);

%Int temp vs time
temp_int = [temp_even' temp_int_odd'];
temp_int = reshape(temp_int', [24 1]);

P_line = polyval(P,0:23);
P_line_space = linspace(0,23,24);

%Plot
figure; 
plot(time,temp,time,temp_int,'r',P_line_space,P_line,'g');

xlim ([0 23])
title('Time VS Temperature');
xlabel('Time','FontSize',10);
ylabel('Temperature(°C)','FontSize',10);

ax = gca;
ax.XTick = time_odd;

%The interpolated values are not close to the acutal values
%However it does have a close general curve as the acutal plot
%The straight line is not a good mode as there are big curves

%% -------------- Task 2 --------------

MSE = zeros(1,9);
for N = 1:9
    
P = polyfit(time_even,temp_even,N);
temp_int_odd = polyval(P,time_odd); %At odd times
MSE(N) = sum((temp_int_odd - temp_odd).^2)/length(temp_odd);
    
end

figure; 
plot(1:9, MSE);

xlim ([1 9]);
title('Polynomial Degree VS Mean Square Error');
xlabel('Polynomial Degree','FontSize',10);
ylabel('Mean Square Error','FontSize',10);

%As the degree of polynomials increase they become better interpolations
%but as the degree incrase past the lowest MSE(6) the behavior becomes wild

%It appears that the 6th degree polynomial produce the best interpolation
%At the 6th degree the MSE is 0.9627

%% -------------- Task 3 --------------

%Nearest Neighbour
temp_n1 = interp1(time_odd,temp_even,time_odd,'nearest');
temp_n = [temp_n1'  temp_even'];
temp_n = reshape(temp_n', [24 1]);

figure; 
plot(time,temp,time,temp_n,'r');

xlim ([0 23])
title('Time VS Temperature');
xlabel('Time','FontSize',10);
ylabel('Temperature(°C)','FontSize',10);

ax = gca;
ax.XTick = time_even;

MSE_neighbour = sum((temp_n1 - temp_odd).^2)/length(temp_odd);

%Yes the curves match up well compared the interpolation in task 1
%but at certain points such as 7:00 the values are still off

%The MSE is very close to the 5th polynomal MSE 
%Compared to task 1 it is alot smaller

%% -------------- Task 4 --------------

%Local Linear Interpolation
temp_L1 = interp1(time_even,temp_even,time_odd,'linear');
temp_L1(12) = temp_even(12);
temp_L = [temp_even' temp_L1' ];
temp_L = reshape(temp_L', [24 1]);

figure; 
plot(time,temp,time,temp_L,'r');

xlim ([0 23])
title('Time VS Temperature');
xlabel('Time','FontSize',10);
ylabel('Temperature(°C)','FontSize',10);

ax = gca;
ax.XTick = time_odd;

MSE_local = sum((temp_L1 - temp_odd).^2)/length(temp_odd);

%The plot of local linear interpolation is the best fit for the orginal
%plot when compared to the plot of task 1 and task 3

%The MSE value is even smaller than the ones computed in task 2
%therefor it is the better method compared the first few

%% -------------- Task 5 --------------

%Piecewise polynomial Interpolation
temp_CSI1 = spline(time_even,temp_even,time_odd);
temp_CSI1(12) = temp_odd(12);
temp_CSI = [temp_even' temp_CSI1' ];
temp_CSI = reshape(temp_CSI', [24 1]);

MSE_CSI = sum((temp_CSI1 - temp_odd).^2)/length(temp_odd);

figure; 
plot(time,temp,time,temp_CSI,'r');

xlim ([0 23])
title('Time VS Temperature');
xlabel('Time','FontSize',10);
ylabel('Temperature(°C)','FontSize',10);

ax = gca;
ax.XTick = time_odd;

%The MSE of cubic sline interpolation is the second lowest MSE overall

%The best interpolation method seems to be the Local Linear Interpolation
%since the MSE is the lowest of the four

