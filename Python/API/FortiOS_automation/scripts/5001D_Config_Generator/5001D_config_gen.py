import re
import os
import sys


def t12_intfX_46(blade, t_num, mdcfg, loopback, subnet=None):
    text = []
    intf1 = 'fabric1'

    text.append("")
    text.append("    edit mgmt1")
    text.append("      set vdom root")
    text.append("      set ip 172.18.10." + blade + "/24")
    text.append("      set allowaccess ping https ssh snmp http telnet fgfm")
    text.append("      set type physical")
    text.append("    next")

    for i in range(11, 18 + 1):
        text.append("    edit v" + str(i))
        text.append("        set vdom root")
        text.append("        set ip " + blade + ".1." + str(i) + ".253 255.255.255.0")
        text.append("        set allowaccess ping")
        text.append("        set interface " + intf1)
        text.append("        set vlanid " + str(i))
        text.append("    next")

    branch = 1
    vlan1 = 11
    vlan2 = 12

    if int(blade) < 120:
        netdata = (int(blade) - 103) * 4
    else:
        netdata = (int(blade) - 103 - 10) * 4

    voice = 1 + netdata
    data = 81 + netdata
    wifi = 161 + netdata
    nettunn = 1 + netdata

    if subnet is not None:
        nettunn = subnet

    for j in range(1, 4 + 1):
        for i in range(1, 250 + 1):

            text.append("    edit br" + str(branch) + "-ISP1")
            text.append("        set vdom br" + str(branch))
            text.append("        set ip " + blade + ".1." + str(vlan1) + "." + str(i) + " 255.255.255.0")
            text.append("        set allowaccess ping")
            text.append("        set type emac-vlan")
            text.append("        set interface v" + str(vlan1))
            text.append("    next")
            text.append("    edit br" + str(branch) + "-ISP2")
            text.append("        set vdom br" + str(branch))
            text.append("        set ip " + blade + ".1." + str(vlan2) + "." + str(i) + " 255.255.255.0")
            text.append("        set allowaccess ping")
            text.append("        set type emac-vlan")
            text.append("        set interface v" + str(vlan2))
            text.append("    next")

            text.append("    edit br" + str(branch) + "-voice")
            text.append("        set vdom br" + str(branch))
            text.append("        set ip 10." + str(voice) + "." + str(i) + ".254 255.255.255.0")
            text.append("        set allowaccess ping")
            text.append("        config ipv6")
            text.append("          set ip6-address 2000::10." + str(voice) + "." + str(i) + ".254/120")
            text.append("          set ip6-allowaccess ping")
            text.append("        end")
            text.append("        set type loopback")
            text.append("    next")
            text.append("    edit br" + str(branch) + "-data")
            text.append("        set vdom br" + str(branch))
            text.append("        set ip 10." + str(data) + "." + str(i) + ".254 255.255.255.0")
            text.append("        set allowaccess ping")
            text.append("        config ipv6")
            text.append("          set ip6-address 2000::10." + str(data) + "." + str(i) + ".254/120")
            text.append("          set ip6-allowaccess ping")
            text.append("        end")
            text.append("        set type loopback")
            text.append("    next")
            text.append("    edit br" + str(branch) + "-wifi")
            text.append("        set vdom br" + str(branch))
            text.append("        set ip 10." + str(wifi) + "." + str(i) + ".254 255.255.255.0")
            text.append("        set allowaccess ping")
            text.append("        config ipv6")
            text.append("          set ip6-address 2000::10." + str(wifi) + "." + str(i) + ".254/120")
            text.append("          set ip6-allowaccess ping")
            text.append("        end")
            text.append("        set type loopback")
            text.append("    next")

            if loopback == 1:
                text.append("    edit br" + str(branch) + "-loopback")
                text.append("        set vdom br" + str(branch))
                text.append("        set ip 10.253." + str(nettunn) + "." + str(i) + " 255.255.255.255")
                text.append("        set allowaccess ping")
                text.append("        config ipv6")
                text.append("          set ip6-address 2000::10.253." + str(nettunn) + "." + str(i) + "/128")
                text.append("          set ip6-allowaccess ping")
                text.append("        end")
                text.append("        set type loopback")
                text.append("    next")

            text.append("    edit br" + str(branch) + "-t1")
            text.append("        set vdom br" + str(branch))

            if mdcfg == 0 and loopback == 0:
                text.append("        set ip 1.1." + str(nettunn) + "." + str(i) + " 255.255.255.255")
                text.append("        set remote-ip 1.1.254.254 255.255.0.0")

            text.append("        set allowaccess ping")
            text.append("        set type tunnel")
            text.append("        config ipv6")

            if mdcfg == 0 and loopback == 0:
                text.append("          set ip6-address 2000::1.1." + str(nettunn) + "." + str(i) + "/112")

            text.append("          set ip6-allowaccess ping")
            text.append("        end")
            text.append("        set interface br" + str(branch) + "-ISP1")
            text.append("    next")
            text.append("    edit br" + str(branch) + "-t3")
            text.append("        set vdom br" + str(branch))

            if mdcfg == 0 and loopback == 0:
                text.append("        set ip 3.3." + str(nettunn) + "." + str(i) + " 255.255.255.255")
                text.append("        set remote-ip 3.3.254.254 255.255.0.0")

            text.append("        set allowaccess ping")
            text.append("        set type tunnel")
            text.append("        config ipv6")

            if mdcfg == 0 and loopback == 0:
                text.append("          set ip6-address 2000::3.3." + str(nettunn) + "." + str(i) + "/112")

            text.append("          set ip6-allowaccess ping")
            text.append("        end")
            text.append("        set interface br" + str(branch) + "-ISP2")
            text.append("    next")

            if t_num == 4:
                text.append("    edit br" + str(branch) + "-t2")
                text.append("        set vdom br" + str(branch))

                if mdcfg == 0 and loopback == 0:
                    text.append("        set ip 2.2." + str(nettunn) + "." + str(i) + " 255.255.255.255")
                    text.append("        set remote-ip 2.2.254.254 255.255.0.0")

                text.append("        set allowaccess ping")
                text.append("        set type tunnel")
                text.append("        config ipv6")

                if mdcfg == 0 and loopback == 0:
                    text.append("          set ip6-address 2000::2.2." + str(nettunn) + "." + str(i) + "/112")

                text.append("          set ip6-allowaccess ping")
                text.append("        end")
                text.append("        set interface br" + str(branch) + "-ISP1")
                text.append("    next")
                text.append("    edit br" + str(branch) + "-t4")
                text.append("        set vdom br" + str(branch))

                if mdcfg == 0 and loopback == 0:
                    text.append("        set ip 4.4." + str(nettunn) + "." + str(i) + " 255.255.255.255")
                    text.append("        set remote-ip 4.4.254.254 255.255.0.0")

                text.append("        set allowaccess ping")
                text.append("        set type tunnel")
                text.append("        config ipv6")

                if mdcfg == 0 and loopback == 0:
                    text.append("          set ip6-address 2000::4.4." + str(nettunn) + "." + str(i) + "/112")

                text.append("          set ip6-allowaccess ping")
                text.append("        end")
                text.append("        set interface br" + str(branch) + "-ISP2")
                text.append("    next")

            branch = branch + 1
            if branch == 1000: break

        vlan1 = vlan1 + 2
        vlan2 = vlan2 + 2
        voice += 1
        data += 1
        wifi += 1
        nettunn += 1

    text.append("end")
    text.append("\n")

    f = open('t12.txt', 'w')
    f.truncate(0)
    f.write('\n'.join(text))
    f.flush()
    f.close()


def t2_vd999_46_mdcfg(blade, t_num, mdcfg, loopback, t1_gwy='100.1.1.204', t2_gwy='100.1.1.204', t3_gwy='100.1.1.204', t4_gwy='100.1.1.204', hc_server='192.168.250.1', subnet=None):
    text = []
    branch = 1
    vlan1 = 11
    vlan2 = 12

    if int(blade) < 120:
        netdata = (int(blade) - 103) * 4
    else:
        netdata = (int(blade) - 103 - 10) * 4

    voice = 1 + netdata
    data = 81 + netdata
    wifi = 161 + netdata
    nettunn = 1 + netdata

    if subnet is not None:
        nettunn = subnet

    for j in range(1, 4 + 1):
        for i in range(1, 250 + 1):

            text.append("config vdom")
            text.append("edit br" + str(branch))

            text.append("  config firewall address")
            text.append("    edit all")
            text.append("    next")
            text.append("    edit subnet1")
            text.append("        set subnet 10." + str(voice) + "." + str(i) + ".0 255.255.255.0")
            text.append("    next")
            text.append("    edit subnet2")
            text.append("        set subnet 10." + str(data) + "." + str(i) + ".0 255.255.255.0")
            text.append("    next")
            text.append("    edit subnet3")
            text.append("        set subnet 10." + str(wifi) + "." + str(i) + ".0 255.255.255.0")
            text.append("    next")
            text.append("    edit t1-ip")
            text.append("        set subnet 1.1." + str(nettunn) + "." + str(i) + " 255.255.255.255")
            text.append("    next")
            text.append("    edit t2-ip")
            text.append("        set subnet 2.2." + str(nettunn) + "." + str(i) + " 255.255.255.255")
            text.append("    next")
            text.append("    edit t3-ip")
            text.append("        set subnet 3.3." + str(nettunn) + "." + str(i) + " 255.255.255.255")
            text.append("    next")
            text.append("    edit t4-ip")
            text.append("        set subnet 4.4." + str(nettunn) + "." + str(i) + " 255.255.255.255")
            text.append("    next")
            text.append("  end")

            text.append("  config firewall address6")
            text.append("    edit all")
            text.append("    next")
            text.append("    edit subnet1")
            text.append("        set ip6 2000::10." + str(voice) + "." + str(i) + ".0/120")
            text.append("    next")
            text.append("    edit subnet2")
            text.append("        set ip6 2000::10." + str(data) + "." + str(i) + ".0/120")
            text.append("    next")
            text.append("    edit subnet3")
            text.append("        set ip6 2000::10." + str(wifi) + "." + str(i) + ".0/120")
            text.append("    next")
            text.append("    edit t1-ip")
            text.append("        set ip6 2000::1.1." + str(nettunn) + "." + str(i) + "/128")
            text.append("    next")
            text.append("    edit t2-ip")
            text.append("        set ip6 2000::2.2." + str(nettunn) + "." + str(i) + "/128")
            text.append("    next")
            text.append("    edit t3-ip")
            text.append("        set ip6 2000::3.3." + str(nettunn) + "." + str(i) + "/128")
            text.append("    next")
            text.append("    edit t4-ip")
            text.append("        set ip6 2000::4.4." + str(nettunn) + "." + str(i) + "/128")
            text.append("    next")
            text.append("  end")

            text.append("  config firewall addrgrp")
            if mdcfg == 0:
                text.append("    edit group1")
                text.append("        set member t1-ip subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group2")
                text.append("        set member t2-ip subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group3")
                text.append("        set member t3-ip subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group4")
                text.append("        set member t4-ip subnet1 subnet2 subnet3")
                text.append("    next")
            else:
                text.append("    edit group1")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group2")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group3")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group4")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
            text.append("  end")

            text.append("  config firewall addrgrp6")
            if mdcfg == 0:
                text.append("    edit group1")
                text.append("        set member t1-ip subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group2")
                text.append("        set member t2-ip subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group3")
                text.append("        set member t3-ip subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group4")
                text.append("        set member t4-ip subnet1 subnet2 subnet3")
                text.append("    next")
            else:
                text.append("    edit group1")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group2")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group3")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
                text.append("    edit group4")
                text.append("        set member subnet1 subnet2 subnet3")
                text.append("    next")
            text.append("  end")

            text.append("  config firewall service category")
            text.append("    edit General")
            text.append("      set comment General")
            text.append("    next")
            text.append("  end")
            text.append("")
            text.append("  config firewall service custom")
            text.append("    edit ALL")
            text.append("      set category General")
            text.append("      set protocol IP")
            text.append("    next")
            text.append("  end")
            text.append("")

            text.append("  config vpn ipsec phase1-interface")
            text.append("    edit br" + str(branch) + "-t1")
            text.append("        set interface br" + str(branch) + "-ISP1")
            text.append("        set ike-version 2")
            text.append("        set peertype any")
            text.append("        set net-device enable")
            if mdcfg != 0:
                text.append("        set mode-cfg enable")
            if loopback == 1:
                text.append("        set exchange-ip-addr4 10.253." + str(nettunn) + '.' + str(i))
                text.append("        set exchange-ip-addr6 2000::10.253." + str(nettunn) + '.' + str(i))
            text.append("        set proposal aes256-sha256")
            text.append("        set localid FGT" + str(blade) + "-br" + str(branch))
            text.append("        set idle-timeout enable")
            text.append("        set auto-discovery-receiver enable")
            text.append("        set network-overlay enable")
            text.append("        set network-id 1")
            text.append("        set remote-gw " + t1_gwy)
            text.append("        set psksecret 123456")
            text.append("        set dpd-retrycount 5")
            text.append("        set dpd-retryinterval 60")
            text.append("    next")

            text.append("    edit br" + str(branch) + "-t3")
            text.append("        set interface br" + str(branch) + "-ISP2")
            text.append("        set ike-version 2")
            text.append("        set peertype any")
            text.append("        set net-device enable")
            if mdcfg != 0:
                text.append("        set mode-cfg enable")
            if loopback == 1:
                text.append("        set exchange-ip-addr4 10.253." + str(nettunn) + '.' + str(i))
                text.append("        set exchange-ip-addr6 2000::10.253." + str(nettunn) + '.' + str(i))
            text.append("        set proposal aes256-sha256")
            text.append("        set localid FGT" + str(blade) + "-br" + str(branch))
            text.append("        set idle-timeout enable")
            text.append("        set auto-discovery-receiver enable")
            text.append("        set network-overlay enable")
            text.append("        set network-id 3")
            text.append("        set remote-gw " + t3_gwy)
            text.append("        set psksecret 123456")
            text.append("        set dpd-retrycount 5")
            text.append("        set dpd-retryinterval 60")
            text.append("    next")

            if t_num == 4:
                text.append("    edit br" + str(branch) + "-t2")
                text.append("        set interface br" + str(branch) + "-ISP1")
                text.append("        set ike-version 2")
                text.append("        set peertype any")
                text.append("        set net-device enable")
                if mdcfg != 0:
                    text.append("        set mode-cfg enable")
                if loopback == 1:
                    text.append("        set exchange-ip-addr4 10.253." + str(nettunn) + '.' + str(i))
                    text.append("        set exchange-ip-addr6 2000::10.253." + str(nettunn) + '.' + str(i))
                text.append("        set proposal aes256-sha256")
                text.append("        set localid FGT" + str(blade) + "-br" + str(branch))
                text.append("        set idle-timeout enable")
                text.append("        set auto-discovery-receiver enable")
                text.append("        set network-overlay enable")
                text.append("        set network-id 2")
                text.append("        set remote-gw " + t2_gwy)
                text.append("        set psksecret 123456")
                text.append("        set dpd-retrycount 5")
                text.append("        set dpd-retryinterval 60")
                text.append("    next")

                text.append("    edit br" + str(branch) + "-t4")
                text.append("        set interface br" + str(branch) + "-ISP2")
                text.append("        set ike-version 2")
                text.append("        set peertype any")
                text.append("        set net-device enable")
                if mdcfg != 0:
                    text.append("        set mode-cfg enable")
                if loopback == 1:
                    text.append("        set exchange-ip-addr4 10.253." + str(nettunn) + '.' + str(i))
                    text.append("        set exchange-ip-addr6 2000::10.253." + str(nettunn) + '.' + str(i))
                text.append("        set proposal aes256-sha256")
                text.append("        set localid FGT" + str(blade) + "-br" + str(branch))
                text.append("        set idle-timeout enable")
                text.append("        set auto-discovery-receiver enable")
                text.append("        set network-overlay enable")
                text.append("        set network-id 4")
                text.append("        set remote-gw " + t4_gwy)
                text.append("        set psksecret 123456")
                text.append("        set dpd-retrycount 5")
                text.append("        set dpd-retryinterval 60")
                text.append("    next")

            text.append("  end")
            text.append("")

            text.append("  config vpn ipsec phase2-interface")
            text.append("    edit br" + str(branch) + "-t1")
            text.append("        set phase1name br" + str(branch) + "-t1")
            text.append("        set proposal aes256-sha256")
            text.append("        set auto-negotiate enable")
            if mdcfg == 1:
                text.append("        set src-addr-type subnet")
                text.append("        set dst-addr-type subnet")
            else:
                text.append("        set src-addr-type name")
                text.append("        set dst-addr-type name")
            if loopback == 1:
                text.append("        set src-name all")
                text.append("        set dst-name all")
            elif mdcfg == 0:
                text.append("        set src-name group1")
                text.append("        set dst-name all")

            text.append("    next")
            text.append("    edit br" + str(branch) + "-t3")
            text.append("        set phase1name br" + str(branch) + "-t3")
            text.append("        set proposal aes256-sha256")
            text.append("        set auto-negotiate enable")
            if mdcfg == 1:
                text.append("        set src-addr-type subnet")
                text.append("        set dst-addr-type subnet")
            else:
                text.append("        set src-addr-type name")
                text.append("        set dst-addr-type name")
            if loopback == 1:
                text.append("        set src-name all")
                text.append("        set dst-name all")
            elif mdcfg == 0:
                text.append("        set src-name group1")
                text.append("        set dst-name all")

            text.append("    next")
            text.append("    edit br" + str(branch) + "-t16")
            text.append("        set phase1name br" + str(branch) + "-t1")
            text.append("        set proposal aes256-sha256")
            text.append("        set auto-negotiate enable")
            if mdcfg == 1:
                text.append("        set src-addr-type subnet6")
                text.append("        set dst-addr-type subnet6")
            else:
                text.append("        set src-addr-type name6")
                text.append("        set dst-addr-type name6")
            if loopback == 1:
                text.append("        set src-name6 all")
                text.append("        set dst-name6 all")
            elif mdcfg == 0:
                text.append("        set src-name6 group1")
                text.append("        set dst-name6 all")

            text.append("    next")
            text.append("    edit br" + str(branch) + "-t36")
            text.append("        set phase1name br" + str(branch) + "-t3")
            text.append("        set proposal aes256-sha256")
            text.append("        set auto-negotiate enable")
            if mdcfg == 1:
                text.append("        set src-addr-type subnet6")
                text.append("        set dst-addr-type subnet6")
            else:
                text.append("        set src-addr-type name6")
                text.append("        set dst-addr-type name6")
            if loopback == 1:
                text.append("        set src-name6 all")
                text.append("        set dst-name6 all")
            elif mdcfg == 0:
                text.append("        set src-name6 group1")
                text.append("        set dst-name6 all")
            text.append("    next")

            if t_num == 4:
                text.append("    edit br" + str(branch) + "-t2")
                text.append("        set phase1name br" + str(branch) + "-t2")
                text.append("        set proposal aes256-sha256")
                text.append("        set auto-negotiate enable")
                if mdcfg == 1:
                    text.append("        set src-addr-type subnet")
                    text.append("        set dst-addr-type subnet")
                else:
                    text.append("        set src-addr-type name")
                    text.append("        set dst-addr-type name")
                if loopback == 1:
                    text.append("        set src-name all")
                    text.append("        set dst-name all")
                elif mdcfg == 0:
                    text.append("        set src-name group1")
                    text.append("        set dst-name all")

                text.append("    next")
                text.append("    edit br" + str(branch) + "-t4")
                text.append("        set phase1name br" + str(branch) + "-t4")
                text.append("        set proposal aes256-sha256")
                text.append("        set auto-negotiate enable")
                if mdcfg == 1:
                    text.append("        set src-addr-type subnet")
                    text.append("        set dst-addr-type subnet")
                else:
                    text.append("        set src-addr-type name")
                    text.append("        set dst-addr-type name")
                if loopback == 1:
                    text.append("        set src-name all")
                    text.append("        set dst-name all")
                elif mdcfg == 0:
                    text.append("        set src-name group1")
                    text.append("        set dst-name all")

                text.append("    next")
                text.append("    edit br" + str(branch) + "-t26")
                text.append("        set phase1name br" + str(branch) + "-t2")
                text.append("        set proposal aes256-sha256")
                text.append("        set auto-negotiate enable")
                if mdcfg == 1:
                    text.append("        set src-addr-type subnet6")
                    text.append("        set dst-addr-type subnet6")
                else:
                    text.append("        set src-addr-type name6")
                    text.append("        set dst-addr-type name6")
                if loopback == 1:
                    text.append("        set src-name6 all")
                    text.append("        set dst-name6 all")
                elif mdcfg == 0:
                    text.append("        set src-name6 group1")
                    text.append("        set dst-name6 all")

                text.append("    next")
                text.append("    edit br" + str(branch) + "-t46")
                text.append("        set phase1name br" + str(branch) + "-t4")
                text.append("        set proposal aes256-sha256")
                text.append("        set auto-negotiate enable")
                if mdcfg == 1:
                    text.append("        set src-addr-type subnet6")
                    text.append("        set dst-addr-type subnet6")
                else:
                    text.append("        set src-addr-type name6")
                    text.append("        set dst-addr-type name6")
                if loopback == 1:
                    text.append("        set src-name6 all")
                    text.append("        set dst-name6 all")
                elif mdcfg == 0:
                    text.append("        set src-name6 group1")
                    text.append("        set dst-name6 all")

                text.append("    next")
            text.append("  end")
            text.append("")

            text.append("  config system sdwan")
            text.append("    set status enable")
            text.append("    config zone")
            text.append("        edit virtual-wan-link")
            text.append("        next")
            text.append("        edit HUB1_OVERLAY")
            text.append("        next")
            text.append("        edit CARRIER1_UNDERLAY")
            text.append("        next")
            text.append("        edit CARRIER2_UNDERLAY")
            text.append("        next")
            text.append("    end")
            text.append("    config members")
            text.append("        edit 1")
            text.append("            set interface br" + str(branch) + "-ISP1")
            text.append("            set zone CARRIER1_UNDERLAY")
            text.append("            set gateway " + str(blade) + ".1." + str(vlan1) + ".254")
            text.append("            set gateway6 2000::" + str(blade) + ".1." + str(vlan1) + ".254")
            text.append("        next")
            text.append("        edit 2")
            text.append("            set interface br" + str(branch) + "-ISP2")
            text.append("            set zone CARRIER2_UNDERLAY")
            text.append("            set gateway " + str(blade) + ".1." + str(vlan2) + ".254")
            text.append("            set gateway6 2000::" + str(blade) + ".1." + str(vlan2) + ".254")
            text.append("        next")
            text.append("        edit 3")
            text.append("            set interface br" + str(branch) + "-t1")
            text.append("            set zone HUB1_OVERLAY")
            text.append("            set priority 20")
            text.append("        next")
            text.append("        edit 5")
            text.append("            set interface br" + str(branch) + "-t3")
            text.append("            set zone HUB1_OVERLAY")
            text.append("            set priority 20")
            text.append("        next")
            if t_num == 4:
                text.append("        edit 4")
                text.append("            set interface br" + str(branch) + "-t2")
                text.append("            set zone HUB1_OVERLAY")
                text.append("            set priority 20")
                text.append("        next")
                text.append("        edit 6")
                text.append("            set interface br" + str(branch) + "-t4")
                text.append("            set zone HUB1_OVERLAY")
                text.append("            set priority 20")
                text.append("        next")

            text.append("    end")
            text.append("    config health-check")
            text.append("        edit DIA")
            text.append("            set server 8.8.4.4 8.8.8.8")
            text.append("            set interval 5000")
            text.append("            set probe-timeout 5000")
            text.append("            set update-static-route disable")
            text.append("            set sla-fail-log-period 10")
            text.append("            set sla-pass-log-period 10")

            text.append("            config sla")
            text.append("                edit 1")
            text.append("                    set latency-threshold 150")
            text.append("                    set jitter-threshold 50")
            text.append("                    set packetloss-threshold 5")
            text.append("                next")
            text.append("            end")
            text.append("        next")
            text.append("        edit HUB1")
            text.append("            set server " + hc_server)
            text.append("            set interval 5000")
            text.append("            set update-static-route disable")
            text.append("            set sla-fail-log-period 10")
            text.append("            set sla-pass-log-period 10")

            if t_num == 4:
                text.append("            set members 3 4 5 6")
            else:
                text.append("            set members 3 5")

            text.append("            config sla")
            text.append("                edit 1")
            text.append("                    set latency-threshold 150")
            text.append("                    set jitter-threshold 50")
            text.append("                next")
            text.append("            end")
            text.append("        next")
            text.append("    end")
            text.append("  end")

            text.append("  config firewall schedule recurring")
            text.append("      edit always")
            text.append("          set day sunday monday tuesday wednesday thursday friday saturday")
            text.append("      next")
            text.append("  end")
            text.append("")

            text.append("  config firewall policy")
            text.append("    edit 1")
            text.append("       set srcintf any")
            text.append("       set dstintf any")
            text.append("       set srcaddr all")
            text.append("       set dstaddr all")
            text.append("       set srcaddr6 all")
            text.append("       set dstaddr6 all")
            text.append("       set action accept")
            text.append("       set schedule always")
            text.append("       set service ALL")
            text.append("    next")
            text.append("  end")
            text.append("")

            text.append("  config router route-map")
            text.append("    edit H1_C1-1")
            text.append("        config rule")
            text.append("            edit 1")
            text.append("                set set-community 64512:1")
            text.append("                unset set-ip-nexthop")
            text.append("                unset set-ip6-nexthop")
            text.append("                unset set-ip6-nexthop-local")
            text.append("                unset set-originator-id")
            text.append("            next")
            text.append("        end")
            text.append("    next")
            text.append("    edit H1_C1-2")
            text.append("        config rule")
            text.append("            edit 1")
            text.append("                set set-community 64512:2")
            text.append("                unset set-ip-nexthop")
            text.append("                unset set-ip6-nexthop")
            text.append("                unset set-ip6-nexthop-local")
            text.append("                unset set-originator-id")
            text.append("            next")
            text.append("        end")
            text.append("    next")
            text.append("    edit H1_C2-1")
            text.append("        config rule")
            text.append("            edit 1")
            text.append("                set set-community 64512:3")
            text.append("                unset set-ip-nexthop")
            text.append("                unset set-ip6-nexthop")
            text.append("                unset set-ip6-nexthop-local")
            text.append("                unset set-originator-id")
            text.append("            next")
            text.append("        end")
            text.append("    next")
            text.append("    edit H1_C2-2")
            text.append("        config rule")
            text.append("            edit 1")
            text.append("                set set-community 64512:4")
            text.append("                unset set-ip-nexthop")
            text.append("                unset set-ip6-nexthop")
            text.append("                unset set-ip6-nexthop-local")
            text.append("                unset set-originator-id")
            text.append("            next")
            text.append("        end")
            text.append("    next")
            text.append("  end")

            text.append("  config router bgp")
            text.append("    set as 64512")
            text.append("    set ibgp-multipath enable")
            text.append("    set additional-path enable")
            text.append("    set additional-path6 enable")
            text.append("    set graceful-restart enable")
            text.append("    set additional-path-select 4")
            text.append("    set additional-path-select6 4")
            text.append("    config neighbor")
            if loopback == 1:
                text.append("        edit 10.253.192.1")
                text.append("            set activate6 disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration enable")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out H1_C1-1")
                text.append("            set update-source br" + str(branch) + "-loopback")
                text.append("            set connect-timer 10")
                text.append("            set additional-path receive")
                text.append("        next")
                text.append("        edit 2000::10.253.192.1")
                text.append("            set activate disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart6 enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration6 enable")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out6 H1_C1-1")
                text.append("            set update-source br" + str(branch) + "-loopback")
                text.append("            set connect-timer 10")
                text.append("            set additional-path6 receive")
                text.append("        next")
            else:
                text.append("        edit 1.1.254.254")
                text.append("            set activate6 disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration enable")
                text.append("            set interface br" + str(branch) + "-t1")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out H1_C1-1")
                text.append("            set connect-timer 10")
                text.append("            set additional-path receive")
                text.append("        next")
                text.append("        edit 3.3.254.254")
                text.append("            set activate6 disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration enable")
                text.append("            set interface br" + str(branch) + "-t3")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out H1_C2-1")
                text.append("            set connect-timer 10")
                text.append("            set additional-path receive")
                text.append("        next")
                text.append("        edit 2000::1.1.254.254")
                text.append("            set activate disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart6 enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration6 enable")
                text.append("            set interface br" + str(branch) + "-t1")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out6 H1_C1-1")
                text.append("            set connect-timer 10")
                text.append("            set additional-path6 receive")
                text.append("        next")
                text.append("        edit 2000::3.3.254.254")
                text.append("            set activate disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart6 enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration6 enable")
                text.append("            set interface br" + str(branch) + "-t3")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out6 H1_C2-1")
                text.append("            set connect-timer 10")
                text.append("            set additional-path6 receive")
                text.append("        next")

            if t_num == 4 and loopback == 0:
                text.append("        edit 2.2.254.254")
                text.append("            set activate6 disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration enable")
                text.append("            set interface br" + str(branch) + "-t2")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out H1_C1-2")
                text.append("            set connect-timer 10")
                text.append("            set additional-path receive")
                text.append("        next")
                text.append("        edit 4.4.254.254")
                text.append("            set activate6 disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration enable")
                text.append("            set interface br" + str(branch) + "-t4")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out H1_C2-2")
                text.append("            set connect-timer 10")
                text.append("            set additional-path receive")
                text.append("        next")
                text.append("        edit 2000::2.2.254.254")
                text.append("            set activate disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart6 enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration6 enable")
                text.append("            set interface br" + str(branch) + "-t2")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out6 H1_C1-2")
                text.append("            set connect-timer 10")
                text.append("            set additional-path6 receive")
                text.append("        next")
                text.append("        edit 2000::4.4.254.254")
                text.append("            set activate disable")
                text.append("            set advertisement-interval 1")
                text.append("            set capability-graceful-restart6 enable")
                text.append("            set link-down-failover enable")
                text.append("            set soft-reconfiguration6 enable")
                text.append("            set interface br" + str(branch) + "-t4")
                text.append("            set remote-as 64512")
                text.append("            set route-map-out6 H1_C2-2")
                text.append("            set connect-timer 10")
                text.append("            set additional-path6 receive")
                text.append("        next")

            text.append("    end")
            text.append("    config network")
            text.append("        edit 1")
            text.append("            set prefix 10." + str(voice) + "." + str(i) + ".0 255.255.255.0")
            text.append("        next")
            text.append("        edit 2")
            text.append("            set prefix 10." + str(data) + "." + str(i) + ".0 255.255.255.0")
            text.append("        next")
            text.append("        edit 3")
            text.append("            set prefix 10." + str(wifi) + "." + str(i) + ".0 255.255.255.0")
            text.append("        next")
            text.append("    end")
            text.append("    config network6")
            text.append("        edit 1")
            text.append("            set prefix 2000::10." + str(voice) + "." + str(i) + ".0/120")
            text.append("        next")
            text.append("        edit 2")
            text.append("            set prefix 2000::10." + str(data) + "." + str(i) + ".0/120")
            text.append("        next")
            text.append("        edit 3")
            text.append("            set prefix 2000::10." + str(wifi) + "." + str(i) + ".0/120")
            text.append("        next")
            text.append("    end")
            text.append("    config redistribute connected")
            text.append("    end")
            text.append("    config redistribute rip")
            text.append("    end")
            text.append("    config redistribute ospf")
            text.append("    end")
            text.append("    config redistribute static")
            text.append("    end  ")
            text.append("    config redistribute isis")
            text.append("    end")
            text.append("    config redistribute6 connected")
            text.append("    end")
            text.append("    config redistribute6 rip")
            text.append("    end")
            text.append("    config redistribute6 ospf")
            text.append("    end")
            text.append("    config redistribute6 static")
            text.append("    end")
            text.append("    config redistribute6 isis")
            text.append("    end")
            text.append("  end")

            text.append("  config router static")
            text.append("      edit 1000")
            text.append("          set distance 1")
            text.append("          set sdwan enable")
            text.append("      next")
            text.append("  end")
            text.append("  config router static6")
            text.append("      edit 1000")
            text.append("          set distance 1")
            text.append("          set sdwan enable")
            text.append("      next")
            text.append("  end")

            text.append("end")
            text.append("")

            branch += 1
            if branch == 1000: break

        vlan1 = vlan1 + 2
        vlan2 = vlan2 + 2
        voice += 1
        data += 1
        wifi += 1
        nettunn += 1

    text.append("\n")
    f = open('t2.txt', 'w')
    f.truncate(0)
    f.write('\n'.join(text))
    f.flush()
    f.close()


if __name__ == '__main__':

    for blade in list(range(103, 113)) + list(range(123, 133)):

        if blade >= 130:
            subnet = -16 * int(blade) + 2320
            loopback = 1
            topo = 2
        else:
            subnet = None
            loopback = 0
            topo = 1

        if blade < 113:
            hostname = 'L_S' + str(blade - 100)
        else:
            hostname = 'R_S' + str(blade - 120)

        print('blade: ' + str(blade), '\nsubnet: ' + str(subnet), '\nhostname: ' + hostname)

        tunnels = 2
        mode_cfg = 1

        t1_gwy = '100.1.1.1' if topo == 2 else '110.1.1.1'
        t3_gwy = '101.1.1.1' if topo == 2 else '111.1.1.1'
        t2_gwy = '102.1.1.1' if topo == 2 else '112.1.1.1'
        t4_gwy = '103.1.1.1' if topo == 2 else '113.1.1.1'
        hc_server = '10.254.62.10' if topo == 2 else '10.254.61.10'

        t12_intfX_46(str(blade), tunnels, mode_cfg, loopback, subnet)
        t2_vd999_46_mdcfg(str(blade), tunnels, mode_cfg, loopback, t1_gwy=t1_gwy, t2_gwy=t2_gwy, t3_gwy=t3_gwy, t4_gwy=t4_gwy, hc_server=hc_server, subnet=subnet)
        f = open('t11.txt', 'r')
        t11 = f.read()
        f.close()
        f = open('t12.txt', 'r')
        t12 = f.read()
        f.close()
        f = open('t13.txt', 'r')
        t13 = f.read()
        f.close()
        f = open('t2.txt', 'r')
        t2 = f.read()
        f.close()

        text = t11.replace("<HOST>", hostname) + t12 + t13 + t2
        ext = ''
        if loopback == 1: ext = ext + '_lb'
        if mode_cfg == 1: ext = ext + '_mdfg'
        if blade == 127: text = text.replace(' 127.1', ' 133.1')

        f = open('blade' + str(blade) + ext + '.conf', 'w')
        f.truncate(0)
        f.write(text)
        f.flush()
        f.close()
