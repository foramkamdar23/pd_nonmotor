addpath('C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\matlab\startup');
add_toolbox_paths;

%03062026
cfg = cfg_emoreg_defaults();

% ===== PATHS =====
cfg.paths.imagesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\Images\NAPS_H';
cfg.paths.scalesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\SAM-Scales';
cfg.paths.resultsDir = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\outputs';
cfg.paths.assetsDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\assets';

%cfg.task.manifestCsv = 'C:\Users\cns-co-admin\Desktop\fk\repos\cp_nonmotor\stimuli\blocks\pilot_block_1.csv';
cfg.task.manifestCsv = 'C:\Users\cns-co-admin\Desktop\fk\repos\cp_nonmotor\stimuli\blocks\pilot_block_2.csv';

% ===== Eyelink =====
cfg.el.useEyelink    = true;


% ===== Millikey =====
cfg.keys.useNumpad = true;

% ===== Screen =====
cfg.screen.screenNumber = 2;

% ===== LOAD MANIFEST =====
manifest = readtable(cfg.task.manifestCsv);

% ===== SELECT TRIGGER SYSTEM =====
cfg.trig.system = 'brainproducts';   % 'biosemi' OR 'brainproducts'

% ===== TRIGGER SETTINGS =====
cfg.trig.portName = 'COM7';        % Confirm in Device Manager
cfg.trig.baud = 2000000;           % REQUIRED for TriggerBox Plus
cfg.trig.useTriggers = true;
cfg.trig.allowDummy  = ~cfg.trig.useTriggers;
%cfg.trig.pulseWidthSec = 0.005;    % 5 ms pulse

% Photodiode
cfg.photo.sizePx = 50;
cfg.photo.marginPx = 10;
cfg.photo.pulseFrames = 2;

% ===== RUN TASK =====
Results = task_emoreg_run(cfg);