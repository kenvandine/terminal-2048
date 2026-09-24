*** Settings ***
Documentation    Test cases for terminal-2048 snap
Resource         kvm.resource
Library          Process


*** Test Cases ***
Terminal 2048 Launches And Renders
    [Documentation]    Verify terminal-2048 snap launches in a foot terminal on Mir
    [Tags]    smoke    yarf:certification_status: blocker
    Start Process    /usr/bin/foot    snap    run    terminal-2048    alias=terminal-2048
    Sleep    3s
    Log Screenshot
    [Teardown]    Terminate Process    terminal-2048
