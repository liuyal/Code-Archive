%% --------------------------- Task 1 ---------------------------

filename = 'baboon.tiff';
%Test lena

X = imread(filename);
Xmat = double (X);

Xsize = size(Xmat);
Length = Xsize(1);
Width = Xsize(2);

y = wextend('2D','sym',Xmat,[1,1]);

[r,c,p]=size(y);

X1 = 0;
for k = 1:p
    for i = 2:r-1
        for j = 2:c-1
            
            m = y(j-1:j+1, i-1:i+1,k);
            n = (sum(m));
            n = round(sum(n)/9);
            
            X1(j,i,k) = n;
        end
    end
end

F={};
for k = 1:p
    
   D = X1(:,:,k);
   D(1,:) = [];
   D(:,1) = [];
    
   F{k} = D;
end

    X1 = cell2mat(F);
    X1 = reshape(X1, [Length Width p]);
    
    X1 = uint8(X1);
    imwrite(X1,'image1.tiff');

    imshow(X1);

    %The image is slightly blurry when compared to the original image
    
    
%% --------------------------- Task 2 ---------------------------

y2 = wextend('2D','sym',Xmat,[2,2]);

[r,c,p]=size(y2);

X2 = 0;
for k = 1:p
    for i = 3:r-2
        for j = 3:c-2
            
            m = y2(j-2:j+2, i-2:i+2,k);
            n = (sum(m));
            n = round(sum(n)/25);
            
            X2(j,i,k) = n;
        end
    end
end

FH={};
for k = 1:p
    
   G = X2(:,:,k);
   G(1:2,:) = [];
   G(:,1:2) = [];
    
   FH{k} = G;
end

    X2 = cell2mat(FH);
    X2 = reshape(X2, [Length Width p]);
    
    X2 = uint8(X2);
    imwrite(X2,'image2.tiff');

    imshow(X2);
    
    %In addition to the increased boarder size, each pixel now takes the 
    %average of 25 surrounding pixels instead of 9 surrounding pixels
    
    %The image is even more blurry when compared to the original image and 
    %Silghtly more blurry when compared to image X1

    
%% --------------------------- Task 3 ---------------------------

H = fspecial('average',[3 3]); 
%H is the same as the 3x3 matrix in task 1

X3_1 = imfilter(X,H,'symmetric','same');
imshow(X3_1);
imwrite(X3_1,'image3_1.tiff'); 
%The resulting image is identical to image obtained from task 1



H2 = fspecial('average',[5 5]);
X3_2 = imfilter(X,H2,'symmetric','same');
imshow(X3_2);
imwrite(X3_2,'image3_2.tiff');
%The resulting image is identical to image obtained from task 2



H3 = fspecial('gaussian',[5 5],2);
X3_3 = imfilter(X,H3,'symmetric','same');
imshow(X3_3);
imwrite(X3_3,'image3_3.tiff');
%When compared to X3_2 and image from task 2 the image is slightly 
%Sharpened and a tiny bit brighter, the difference is almost unnoticeable


%% --------------------------- Task 4 ---------------------------

Xb = double(X2);

filter = fspecial('gaussian',[5 5],2);
Xg = imfilter(Xb,filter,'symmetric','same');

c = 0.55;
X4 = ((c/(2*c-1))* Xb)-(((1-c)/(2*c-1))*Xg);
X4 = uint8(X4);

imshow(X4);
imwrite(X4,'image4.tiff');

%The resulting image does look sharper than the image from task 2
%It appears that the best value of to sharpen was 0.55



