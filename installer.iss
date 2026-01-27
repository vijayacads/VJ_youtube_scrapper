; Inno Setup Installer Script for VJ Youtube Amaze
; This creates a Windows installer with shortcuts

[Setup]
AppName=VJ Youtube Amaze
AppVersion=1.0
AppPublisher=VJ Youtube Amaze
DefaultDirName={autopf}\VJ Youtube Amaze
DefaultGroupName=VJ Youtube Amaze
AllowNoIcons=yes
LicenseFile=
OutputDir=dist
OutputBaseFilename=VJ_Youtube_Amaze_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=
UninstallDisplayIcon={app}\VJ_Youtube_Amaze.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\VJ_Youtube_Amaze.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\static\*"; DestDir: "{app}\static"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\VJ Youtube Amaze"; Filename: "{app}\VJ_Youtube_Amaze.exe"
Name: "{group}\{cm:UninstallProgram,VJ Youtube Amaze}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\VJ Youtube Amaze"; Filename: "{app}\VJ_Youtube_Amaze.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\VJ Youtube Amaze"; Filename: "{app}\VJ_Youtube_Amaze.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\VJ_Youtube_Amaze.exe"; Description: "{cm:LaunchProgram,VJ Youtube Amaze}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel1.Caption := 'Welcome to VJ Youtube Amaze Setup';
  WizardForm.WelcomeLabel2.Caption := 'This will install VJ Youtube Amaze on your computer.' + #13#10 + #13#10 +
    'You will be able to scrape YouTube videos, get transcripts, and export channel data with ease.';
end;
