load("C:\Users\fkamdar\Desktop\cerebellar_project\ucsf Feb 17 2025 visit\emotion_regulation_task\Results\Results_Y3_S1_17-Feb-2026.mat");

load("C:\Users\fkamdar\Desktop\cerebellar_project\UCSF Testing Visits\ucsf Feb 17 2026 visit\emotion_regulation_task\Results\Results_Y1_S1_17-Feb-2026.mat")
TL = Results.TriggerLog;

% Get unique trials excluding intro (trial 0)
trialIDs = unique([TL.trial]);
trialIDs(trialIDs == 0) = [];

nTrials = length(trialIDs);
trialDuration = nan(nTrials,1);

for i = 1:nTrials
    tID = trialIDs(i);
    
    % indices for this trial
    idx = find([TL.trial] == tID);
    phases = {TL(idx).phase};
    times  = [TL(idx).tGetSecs];
    
    % find fix1 (start)
    startIdx = find(strcmp(phases,'fix1'),1,'first');
    
    % find valence_response (end)
    endIdx = find(strcmp(phases,'valence_response'),1,'last');
    
    if ~isempty(startIdx) && ~isempty(endIdx)
        trialDuration(i) = times(endIdx) - times(startIdx);
    end
end

% Display
table(trialIDs', trialDuration)

trialDuration = trialDuration(1:end-1);
trialIDs= trialIDs';
trialIDs = trialIDs(1:end-1);

fprintf('\n===== Trial Duration Statistics =====\n');
fprintf('Number of trials: %d\n', length(trialDuration));
fprintf('Mean duration: %.3f seconds\n', mean(trialDuration));
fprintf('Std duration : %.3f seconds\n', std(trialDuration));
fprintf('Min duration : %.3f seconds\n', min(trialDuration));
fprintf('Max duration : %.3f seconds\n', max(trialDuration));
fprintf('=====================================\n\n');