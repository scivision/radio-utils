function [m,t] = fmdemod_complex(y,fs,fc,fmdev)
arguments
    y (:,1)
    fs (1,1) {mustBeInteger,mustBePositive}
    fc (1,1) = []
    fmdev (1,1) {mustBePositive} = 75e3
end
%FMDEMOD Frequency demodulation of complex IQ baseband.

t =(0:length(y)-1)/fs;
%% freq shift if necessary
if ~isempty(fc)
    y = y .* exp(-1i*2*pi*fc*t).';
    disp(['used carrier offset [Hz]',num2str(fc)])
end
%% fm demodulation
m = fs/(2*pi*fmdev) * [0; diff(unwrap(angle(y)))];
end
