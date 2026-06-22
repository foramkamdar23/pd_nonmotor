addpath('C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\matlab\startup');
add_toolbox_paths;

%03062026
cfg = cfg_emoreg_defaults();

%CHANGE if needed
cfg.task.manifestCsv = 'C:\Users\cns-co-admin\Desktop\fk\repos\pd_nonmotor\stimuli\blocks\pdnm064_sessions\PDNM064_session_5_block_112.csv';
cfg.block     = 2;

% ===== SUBJECT =====
cfg.subject   = 'PDNM064';
cfg.session   = 5;
cfg.condition = 5;


% ===== SELECT TRIGGER SYSTEM =====
cfg.trig.system = 'brainproducts';  

% ===== TRIGGER SETTINGS =====
cfg.trig.portName = 'COM7';        % Confirm in Device Manager
cfg.trig.baud = 2000000;           % REQUIRED for TriggerBox Plus
cfg.trig.useTriggers = true;
cfg.trig.allowDummy  = ~cfg.trig.useTriggers;

% ===== PATHS =====
cfg.paths.imagesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\Images\NAPS_H';
cfg.paths.scalesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\SAM-Scales';
cfg.paths.resultsDir = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\outputs';
cfg.paths.assetsDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\assets';


% ===== Eyelink =====clcclccc
cfg.el.useEyelink = true;


% ===== Millikey =====
cfg.keys.useNumpad = true;

% ===== Screen =====
cfg.screen.screenNumber = 2;

% ===== LOAD MANIFEST =====
manifest = readtable(cfg.task.manifestCsv);

% Photodiode
cfg.photo.sizePx = 50;
cfg.photo.marginPx = 10;
cfg.photo.pulseFrames = 2;

% ===== RUN TASK =====
Results = task_emoreg_run(cfg);