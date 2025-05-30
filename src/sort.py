from pathlib import Path

import pybase64


def generate_header_text(protocol_name, protocols):
    profile_title = f"🌐 V2Ray Reaper | {protocols.get(protocol_name, '')} 🔐"
    encoded_title = pybase64.b64encode(profile_title.encode()).decode()
    return f"""#profile-title: base64:{encoded_title}
#profile-update-interval: 1
#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=2546249531
#support-url: https://github.com/sclyxcn/v2ray-reaper
#profile-web-page-url: https://github.com/sclyxcn/v2ray-reaper
"""


def main() -> None:
    protocols = {
        "vmess": "vmess",
        "vless": "vless",
        "trojan": "trojan",
        "ss": "ss",
        "ssr": "ssr",
        "tuic": "tuic",
        "hy2": "hysteria2",
        "warp": "warp",
        "all": "all",
    }

    base_path = Path(__file__).parent.parent
    split_path = base_path / "protocol"
    split_path.mkdir(exist_ok=True)

    protocol_data = {protocol: generate_header_text(protocol, protocols) for protocol in protocols}
    
    with (base_path / "normal" / "mix").open("r") as f:
        for config in f.readlines():
            for protocol in protocols:
                if protocol != "all":
                    if config not in protocol_data["all"]:
                        protocol_data["all"]+=f"{config}"
                    if config.startswith(protocol):
                        protocol_data[protocol] += f"{config}"
                        break

    
    for protocol, data in protocol_data.items():
        try:
            encoded_data = pybase64.b64encode(data.encode()).decode()
            with (split_path / protocols[protocol]).open("w") as file:
                file.write(encoded_data)
        except IsADirectoryError as e:
            print(f"{Fore.RED}Failed{Fore.RESET} Error: {e}. The path '{split_path / protocols[protocol]}' is a directory, not a file.")
            continue



if __name__ == "__main__":
    main()
