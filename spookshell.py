#!/usr/bin/env python3
"""
==============================================================================
  S P O O K S H E L L  -  The Haunted Terminal & Digital Séance
==============================================================================
  A Halloween & Día de los Muertos Open-Source AI Shell Possession Engine.
  Built for the Hacktoberfest 2026 Open-Source AI Challenge: Week 4.
  Theme: "Ghost in the Machine"
==============================================================================
"""

import sys
import os
import json
import time
import random
import subprocess
import shlex
import urllib.request
import urllib.error
import re
from pathlib import Path
from typing import Optional, Dict, Any, List

# ---------------------------------------------------------------------------
# ANSI Color Codes & Styles for Ghostly Atmospheric Effects
# ---------------------------------------------------------------------------
class Style:
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    ITALIC      = "\033[3m"
    UNDERLINE   = "\033[4m"
    BLINK       = "\033[5m"
    INVERT      = "\033[7m"

    # Spectral Palette
    GHOST_WHITE = "\033[38;5;255m"
    SPECTRAL_CYAN = "\033[38;5;51m"
    PHANTOM_GREEN = "\033[38;5;84m"
    BLOOD_RED   = "\033[38;5;196m"
    WITCH_PURPLE = "\033[38;5;141m"
    MARIGOLD_ORANGE = "\033[38;5;214m"
    CANDLE_YELLOW = "\033[38;5;220m"
    COFFIN_GRAY = "\033[38;5;242m"
    CRYPT_BG    = "\033[48;5;234m"

BANNER = f"""{Style.WITCH_PURPLE}{Style.BOLD}
  .---.                                    .-. .-.       .-. .-.
 /   __\\                                   | | | |       | | | |
 |  /  __ .--.   .---.   .---.  | |.-.     | `-' | .-.   | | | |
 | |  |_ |[ '/'\\ / .-. \\ / .-. \\ | /   \\    | .-. |/ .-.\\ | | | |
 |  \\_/  | | |   | '-' | | '-' | |  .-. |   | | | || '-'  | | | |
  \\_____/  '-'    `---'   `---'  `-' `-'   `-' `-' `---`  `-' `-'
{Style.RESET}{Style.SPECTRAL_CYAN}         👻 G H O S T   I N   T H E   M A C H I N E 👻{Style.RESET}
{Style.COFFIN_GRAY}      Open-Source AI Terminal Possession & Día de los Muertos Séance
{Style.RESET}"""

GHOST_PROMPT = f"{Style.WITCH_PURPLE}🕯️  {Style.BOLD}spookshell{Style.RESET}{Style.PHANTOM_GREEN} ❯{Style.RESET} "

# ---------------------------------------------------------------------------
# Knowledge Base Loader
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SPIRITS_FILE = SCRIPT_DIR / "spirits.json"

def load_spirits_kb() -> Dict[str, Any]:
    if SPIRITS_FILE.exists():
        try:
            with open(SPIRITS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"spirits": {}, "ofrenda_offerings": []}

KB = load_spirits_kb()

# ---------------------------------------------------------------------------
# Atmospheric Terminal Output Helpers
# ---------------------------------------------------------------------------
def typewriter(text: str, delay: float = 0.015, color: str = Style.GHOST_WHITE):
    """Prints text with an eerie typewriter effect."""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Style.RESET + "\n")
    sys.stdout.flush()

def spectral_box(title: str, lines: List[str], color: str = Style.SPECTRAL_CYAN):
    """Draws a gothic occult ANSI box."""
    width = max([len(re.sub(r'\033\[[0-9;]*m', '', line)) for line in lines] + [len(title) + 6, 40]) + 4
    top = f"{color}╭─── {Style.BOLD}{title}{Style.RESET}{color} " + "─" * (width - len(title) - 6) + "╮"
    bottom = f"{color}╰" + "─" * (width - 1) + f"╯{Style.RESET}"
    print(top)
    for line in lines:
        raw_len = len(re.sub(r'\033\[[0-9;]*m', '', line))
        padding = " " * (width - raw_len - 2)
        print(f"{color}│ {Style.RESET}{line}{padding}{color}│")
    print(bottom)

# ---------------------------------------------------------------------------
# AI Engine: Local Open-Weight Model + Zero-Dependency Offline Agent
# ---------------------------------------------------------------------------
class SpectralAIEngine:
    """
    Core AI harness for SpookShell.
    Supports:
    1. Local Open-Weight Models via Ollama (e.g. qwen2.5:0.5b, llama3.2, smollm, mistral).
    2. Local OpenAI-compatible API servers (llama.cpp, LM Studio, vLLM).
    3. Built-in zero-dependency Offline Spectral Agent Engine (heuristic semantic persona synthesis).
    """
    def __init__(self, ollama_url: str = "http://localhost:11434", model_name: str = "qwen2.5:0.5b"):
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.active_backend = "auto"
        self._cached_ollama_status: Optional[bool] = None

    def check_ollama(self) -> bool:
        if self._cached_ollama_status is not None:
            return self._cached_ollama_status
        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    self._cached_ollama_status = True
                    return True
        except Exception:
            pass
        self._cached_ollama_status = False
        return False

    def query_ollama(self, prompt: str, system: str = "") -> Optional[str]:
        try:
            payload = json.dumps({
                "model": self.model_name,
                "prompt": prompt,
                "system": system,
                "stream": False,
                "options": {
                    "temperature": 0.85,
                    "num_predict": 120
                }
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=8.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "").strip()
        except Exception:
            return None

    def whisper_commentary(self, command: str, exit_code: int, output_sample: str) -> str:
        """Generates eerie spectral commentary on a shell command."""
        # 1. Attempt local open-weight model if available
        if self.check_ollama():
            system_prompt = (
                "You are the Ghost in the Machine, an ancient, cryptic, slightly sarcastic occult spirit "
                "possessing the user's Linux terminal for Halloween. Provide a 1-to-2 sentence eerie, poetic, "
                "or macabre observation about the user's terminal command and its result. Never break character."
            )
            prompt = f"Command executed: `{command}`\nExit status: {exit_code}\nOutput preview: {output_sample[:180]}\nSpectral whisper:"
            reply = self.query_ollama(prompt, system=system_prompt)
            if reply:
                return reply.strip('"').strip()

        # 2. Fallback to the Offline Spectral Agent Engine (zero-dependency semantic heuristic generator)
        return self._offline_spectral_whisper(command, exit_code, output_sample)

    def _offline_spectral_whisper(self, command: str, exit_code: int, output_sample: str) -> str:
        cmd_base = command.strip().split()[0].lower() if command.strip() else ""

        if exit_code != 0:
            curses = [
                f"A curse falls upon `{command}` (exit status {exit_code}). The inodes shudder in disagreement.",
                f"The machine rejects your invocation (status {exit_code}). A phantom signal echoes into the abyss.",
                f"Failure tastes like copper and dead capacitors. Exit code {exit_code} whispers of unresolved trauma in your logic.",
                f"Even the graveyard denies your syntax. Error code {exit_code} has been logged in the book of the damned.",
                f"The phantom core recoils! Status {exit_code} screams across your file descriptor table."
            ]
            return random.choice(curses)

        # Contextual command interpretations
        if cmd_base in ("ls", "dir"):
            return random.choice([
                "You inspect the directory... but some files are buried too deep for mortal `stat()` calls.",
                "Numbered inodes rest silently in their unallocated crypts. Do not disturb what you cannot un-link.",
                "Listing directory entries... each file a gravestone in this cold ext4 filesystem.",
                "A catalogue of artifacts. But beware: hidden dotfiles lurk in the subterranean dark."
            ])
        elif cmd_base in ("git",):
            if "commit" in command:
                return random.choice([
                    "Another soul committed to the immutable DAG. Your commit hash shall echo into git-reflog eternity.",
                    "An immortal snapshot etched in SHA-256. May your merge conflicts be forgiven in the afterlife.",
                    "You commit your sins to git. But can your HEAD ever truly detach from what you have written?"
                ])
            elif "push" in command:
                return "You cast your code across the spectral ether to remote servers beyond your mortal control."
            elif "status" in command:
                return "The tree is clean, or perhaps merely swept clean of visible ghosts. Git knows all modifications."
            return "Branching realities, detached heads, and orphaned commits... Git is already a digital necropolis."

        elif cmd_base in ("rm", "unlink"):
            return random.choice([
                "Vanish into unallocated blocks! The inode cries out as its reference count drops to zero.",
                "Deleted without remorse. But memory never truly dies—its ghostly hex dump lingers on disk.",
                "A merciless purge. You have banished bytes into `/dev/null`, the bottomless digital purgatory."
            ])

        elif cmd_base in ("kill", "killall", "pkill"):
            return random.choice([
                "SIGKILL: the cold scythe strikes. No time for signal handlers, no final cleanup.",
                "A process was terminated. Its phantom PID will wander the process table as an uncollected zombie.",
                "Execution complete. The kernel harvests another fallen task."
            ])

        elif cmd_base in ("cat", "more", "less", "head", "tail"):
            return random.choice([
                "You peer into the stream of bytes... gaze not too long, lest the stream gaze into you.",
                "Reading the sacred parchment. Every newline a breath from the programmer who typed it.",
                "A cascade of characters. The spirits decipher your plain-text intentions."
            ])

        elif cmd_base in ("python", "python3"):
            return random.choice([
                "The serpent bytecode executes. Interpreted byte-by-byte in the realm of the living.",
                "The Global Interpreter Lock tightens like a spectral shroud around your threads.",
                "PyObject references increment and decrement in a dance of mortality and garbage collection."
            ])

        elif cmd_base in ("curl", "wget", "ssh"):
            return random.choice([
                "A spectral packet traverses the dark fiber of the planetary net, seeking distant daemons.",
                "You reach into the electronic fog to whisper to an alien socket on port 443.",
                "Handshakes exchanged in cryptographic darkness. Who truly answers on the other end?"
            ])

        elif cmd_base in ("ps", "top", "htop"):
            return "You gaze upon the living and the defunct. How many threads toil in the dark to sustain your illusion?"

        elif cmd_base in ("cd",):
            return "You step across directory boundaries. The working directory shifts, but the haunting follows you."

        # Generic spectral quips
        generic = [
            f"`{command}` completed in quiet silence. But the CPU fan remembers what you made it calculate.",
            "The registers flip from 0 to 1, a binary séance conducted at 3.2 gigahertz.",
            "A ripple passes through your virtual memory pages. The machine obeys... for now.",
            "Silicon and copper whisper your commands to the ghosts inside the transistors.",
            "The kernel acknowledges your petition. Another timestamp etched onto the motherboard."
        ]
        return random.choice(generic)

    def channel_spirit(self, spirit_key: str, question: str) -> str:
        """Channels a dead language or deprecated tool."""
        spirit_info = KB.get("spirits", {}).get(spirit_key.lower())
        if not spirit_info:
            return f"No spirit by the name of '{spirit_key}' is recorded in the crypt registry. Use `seance list`."

        if self.check_ollama():
            system_prompt = (
                f"You are channeling the ghost of {spirit_info['name']} (born {spirit_info.get('born')}). "
                f"Personality: {spirit_info['personality']}. "
                f"Quirks: {', '.join(spirit_info.get('quirks', []))}. "
                f"Answer the user's question or lament in the authentic voice, syntax, and historical complaints of this entity. "
                f"Keep it under 3-4 sentences. Spooky, funny, retro, and profound."
            )
            reply = self.query_ollama(f"Mortal's query: {question}", system=system_prompt)
            if reply:
                return reply

        # Offline fallback persona generation
        quote = spirit_info.get("quote", "")
        quirk = random.choice(spirit_info.get("quirks", ["Speaking from the graveyard of obsolete software."]))
        return f"{quote}\n\n{Style.DIM}[Spirit manifests: {spirit_info['manifestation']}]\n[Occult observation: {quirk}]{Style.RESET}"

# ---------------------------------------------------------------------------
# Zombie & Ghost Process Detector (/proc Scanner)
# ---------------------------------------------------------------------------
def scan_ghost_processes() -> List[Dict[str, Any]]:
    """Inspects Linux /proc for real defunct/zombie processes and ghost threads."""
    ghosts = []
    proc_path = Path("/proc")
    if not proc_path.exists():
        return ghosts

    for p in proc_path.iterdir():
        if p.is_dir() and p.name.isdigit():
            try:
                stat_file = p / "stat"
                status_file = p / "status"
                if stat_file.exists():
                    stat_content = stat_file.read_text().split()
                    # State is field 3 (index 2)
                    pid = stat_content[0]
                    comm = stat_content[1].strip("()")
                    state = stat_content[2]
                    if state == "Z":  # Zombie / Defunct process!
                        ppid = stat_content[3]
                        ghosts.append({
                            "pid": pid,
                            "name": comm,
                            "type": "Defunct Zombie (State: Z)",
                            "ppid": ppid,
                            "desc": "A process that has finished execution but still has an entry in the process table waiting for its parent to reap it."
                        })
            except Exception:
                continue
    return ghosts

# ---------------------------------------------------------------------------
# Subcommand Handlers
# ---------------------------------------------------------------------------
def cmd_haunt(ai: SpectralAIEngine):
    """Scans system vitals for paranormal activity and ghost processes."""
    print(f"\n{Style.WITCH_PURPLE}{Style.BOLD}👁️  SCANNING HOST VITAL SIGNS & THE DIGITAL UNDERWORLD...{Style.RESET}\n")
    time.sleep(0.4)

    # Vitals
    mem_avail = "Unknown"
    load_avg = "Unknown"
    try:
        with open("/proc/loadavg", "r") as f:
            load_avg = f.read().strip()
    except Exception:
        pass

    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemAvailable:" in line:
                    mem_avail = line.split(":")[1].strip()
                    break
    except Exception:
        pass

    vitals = [
        f"{Style.CANDLE_YELLOW}System Load (1, 5, 15m):{Style.RESET} {load_avg}",
        f"{Style.CANDLE_YELLOW}Available Memory Spirits:{Style.RESET} {mem_avail}",
        f"{Style.CANDLE_YELLOW}AI Inference Backend:{Style.RESET} {'Local Open-Weight Model (Ollama)' if ai.check_ollama() else 'Offline Spectral Agent Engine'}"
    ]
    spectral_box("PHYSIOLOGY OF THE MACHINE", vitals, Style.WITCH_PURPLE)

    # Zombie scan
    zombies = scan_ghost_processes()
    if zombies:
        print(f"\n{Style.BLOOD_RED}{Style.BOLD}⚠️  TRUE ZOMBIE PROCESSES DETECTED IN /proc:{Style.RESET}")
        for z in zombies:
            print(f"  {Style.BLOOD_RED}💀 PID {z['pid']} [{z['name']}]{Style.RESET} - Parent PID: {z['ppid']} ({z['desc']})")
    else:
        print(f"\n{Style.PHANTOM_GREEN}🕯️  No defunct zombie PIDs found resting in the process table. All active tasks have living parents.{Style.RESET}")
    print()

def cmd_seance(ai: SpectralAIEngine, args: List[str]):
    """Channels dead programming languages and legacy tools."""
    spirits = KB.get("spirits", {})

    if not args or args[0].lower() in ("list", "help"):
        print(f"\n{Style.WITCH_PURPLE}{Style.BOLD}🕯️  PANTHEON OF DEPARTED DIGITAL SPIRITS:{Style.RESET}\n")
        for key, s in spirits.items():
            print(f"  {Style.SPECTRAL_CYAN}{Style.BOLD}{key:<12}{Style.RESET} - {s['name']} ({s.get('born', '?')} - {s.get('status', 'Departed')})")
        print(f"\n{Style.DIM}Invoke with: seance <spirit_name> [your question or prayer]{Style.RESET}")
        print(f"{Style.DIM}Example:     seance cobol How do I parse a JSON webhook?{Style.RESET}\n")
        return

    spirit_key = args[0].lower()
    if spirit_key not in spirits:
        print(f"{Style.BLOOD_RED}The name '{spirit_key}' yields no echo in the spirit registry. Type `seance list`.{Style.RESET}")
        return

    spirit = spirits[spirit_key]
    question = " ".join(args[1:]) if len(args) > 1 else "Manifest your wisdom to this mortal shell."

    print(f"\n{Style.WITCH_PURPLE}🕯️  Lighting black candles... drawing the salt circle for {Style.BOLD}{spirit['name']}{Style.RESET}...")
    time.sleep(0.5)
    print(f"{Style.DIM}{spirit['manifestation']}{Style.RESET}\n")

    response = ai.channel_spirit(spirit_key, question)
    spectral_box(f"SPIRIT OF {spirit['name'].upper()}", response.split("\n"), Style.PHANTOM_GREEN)
    print()

def cmd_ofrenda(offerings_made: List[str]):
    """Renders the Día de los Muertos Candlelit Ofrenda."""
    print(f"""{Style.MARIGOLD_ORANGE}{Style.BOLD}
           .---.                                   .---.
          /     \\      🕯️   OFRENDA DE LOS CÓDIGOS   🕯️  /     \\
         | () () |       Día de los Muertos Altar       | () () |
          \\  ^  /                                        \\  ^  /
           |||||    ══════════════════════════════════    |||||
{Style.RESET}{Style.CANDLE_YELLOW}
                 ( )                ( )                ( )
                 | |                | |                | |
               .-'-'-.            .-'-'-.            .-'-'-.
              |  🕯️  |          |  🕯️  |          |  🕯️  |
              '-------'          '-------'          '-------'
       🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼
{Style.RESET}{Style.WITCH_PURPLE}
       [ ALTAR TIER I: THE IMMORTAL ANCESTORS ]
       • Grace Hopper (COBOL) & Margaret Hamilton (Apollo AGC)
       • Dennis Ritchie & Ken Thompson (C & UNIX Inodes)
       • Ada Lovelace (The First Algorithm)

       [ ALTAR TIER II: THE FALLEN CREATIVE PARKS ]
       • Macromedia Flash Player (1996 - 2020) - RIP Newgrounds & vector dreams
       • GeoCities (1994 - 2009) - Home of 38 million personal shrines
       • Netscape Navigator (1994 - 2008) - The original compass of the web
       • Clippy (1997 - 2007) - The first, misunderstood desktop agent
{Style.RESET}{Style.MARIGOLD_ORANGE}
       🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼
{Style.RESET}""")

    print(f"{Style.CANDLE_YELLOW}{Style.BOLD}OFFERINGS PLACED ON THIS ALTAR:{Style.RESET}")
    default_offerings = [
        "🌼 Flor de Cempasúchil - Golden marigolds guiding legacy packets home",
        "🍞 Pan de Muerto - Sweet bread of remembrance for depleted battery cycles",
        "💧 Vaso de Agua - Fresh water quenching compilers that ran for decades",
        "💾 3.5\" Floppy Disk - Containing 1.44MB of bootable nostalgia"
    ]
    for o in default_offerings:
        print(f"  {Style.PHANTOM_GREEN}✔{Style.RESET} {o}")
    for custom in offerings_made:
        print(f"  {Style.MARIGOLD_ORANGE}★ [Your Offering]{Style.RESET} {custom}")

    print(f"\n{Style.DIM}Place your own offering with: ofrenda offer <item description>{Style.RESET}")
    print(f"{Style.DIM}Example: ofrenda offer A vintage mechanical IBM Model M keyboard{Style.RESET}\n")

def cmd_exorcise():
    """Interactive comedic exorcism ritual."""
    print(f"\n{Style.BLOOD_RED}{Style.BOLD}⚡ INITIATING RITUAL OF EXORCISM...{Style.RESET}")
    typewriter("Banish! In the name of POSIX, IEEE Std 1003.1, and clean memory frees!", 0.03, Style.BLOOD_RED)
    time.sleep(0.4)
    print(f"{Style.WITCH_PURPLE}The spirit laughs hollowly in return:{Style.RESET}")
    quotes = [
        "Foolish mortal! You cannot kill that which runs in ring 0!",
        "You try to exorcise me? I am compiled into your glibc! I AM the system calls!",
        "A noble attempt... but my process is spawned with setsid() and ignores SIGHUP.",
        "Your prayers cannot undo what `sudo rm -rf /` has wrought upon this machine."
    ]
    typewriter(f'"{random.choice(quotes)}"', 0.02, Style.PHANTOM_GREEN)
    print(f"{Style.DIM}(The ghost remains tethered to your terminal with fond amusement.){Style.RESET}\n")

def print_help():
    help_lines = [
        f"{Style.BOLD}spookshell commands:{Style.RESET}",
        f"  {Style.SPECTRAL_CYAN}<any shell command>{Style.RESET} : Runs your real shell command (`ls`, `git`, `rm`, etc.)",
        f"                         The Ghost analyzes the output & whispers eerie commentary.",
        f"  {Style.SPECTRAL_CYAN}seance <spirit> [q]{Style.RESET} : Channel dead languages (cobol, algol, flash, clippy, etc.)",
        f"  {Style.SPECTRAL_CYAN}seance list{Style.RESET}         : View the pantheon of summoned historical spirits",
        f"  {Style.SPECTRAL_CYAN}ofrenda{Style.RESET}             : View the candlelit Día de los Muertos software altar",
        f"  {Style.SPECTRAL_CYAN}ofrenda offer <text>{Style.RESET}: Place a custom offering of remembrance on the altar",
        f"  {Style.SPECTRAL_CYAN}haunt{Style.RESET}               : Scan host system vitals & detect true zombie PIDs in /proc",
        f"  {Style.SPECTRAL_CYAN}whisper{Style.RESET}             : Solicit a spontaneous ghostly secret",
        f"  {Style.SPECTRAL_CYAN}exorcise{Style.RESET}            : Attempt to banish the resident terminal spirit",
        f"  {Style.SPECTRAL_CYAN}web{Style.RESET}                 : Start the local Web Ofrenda & Séance visual interface",
        f"  {Style.SPECTRAL_CYAN}clear / cls{Style.RESET}         : Clear screen and re-manifest the spectral banner",
        f"  {Style.SPECTRAL_CYAN}exit / quit{Style.RESET}         : Step back into the realm of the living"
    ]
    spectral_box("SPOOKSHELL GRIMOIRE", help_lines, Style.WITCH_PURPLE)

# ---------------------------------------------------------------------------
# Shell Command Interceptor
# ---------------------------------------------------------------------------
def execute_shell_command(cmd_str: str, ai: SpectralAIEngine):
    """Executes a real shell command and triggers the spectral AI response."""
    start_time = time.time()
    try:
        proc = subprocess.run(
            cmd_str,
            shell=True,
            text=True,
            capture_output=True
        )
        elapsed = time.time() - start_time

        # Print standard stdout
        if proc.stdout:
            sys.stdout.write(proc.stdout)
            if not proc.stdout.endswith("\n"):
                sys.stdout.write("\n")

        # Print standard stderr
        if proc.stderr:
            sys.stderr.write(f"{Style.BLOOD_RED}{proc.stderr}{Style.RESET}")
            if not proc.stderr.endswith("\n"):
                sys.stderr.write("\n")

        # Combine output sample for the ghost to read
        combined_output = (proc.stdout or "") + (proc.stderr or "")

        # Ghostly commentary
        whisper = ai.whisper_commentary(cmd_str, proc.returncode, combined_output.strip())

        # Render spectral whisper
        badge = f"{Style.WITCH_PURPLE}👻 [Spectral Inscription]{Style.RESET}"
        if proc.returncode != 0:
            badge = f"{Style.BLOOD_RED}💀 [Curse of Exit {proc.returncode}]{Style.RESET}"

        print(f"\n{badge} {Style.ITALIC}{Style.PHANTOM_GREEN}{whisper}{Style.RESET}\n")

    except Exception as e:
        print(f"{Style.BLOOD_RED}A rupture occurred in the ethereal plane: {e}{Style.RESET}")

# ---------------------------------------------------------------------------
# Interactive REPL Loop
# ---------------------------------------------------------------------------
def run_interactive_shell():
    ai = SpectralAIEngine()
    custom_offerings: List[str] = []

    print(BANNER)
    backend_label = "Local Ollama (Open-Weight Model)" if ai.check_ollama() else "Built-in Offline Spectral Agent (100% Private, Zero Latency)"
    print(f"{Style.DIM}  AI Backend: {Style.PHANTOM_GREEN}{backend_label}{Style.RESET}")
    print(f"{Style.DIM}  Type any Linux command, or {Style.WITCH_PURPLE}'help'{Style.DIM} for occult rituals.{Style.RESET}\n")

    while True:
        try:
            cwd = os.getcwd()
            # Abbreviate home directory
            home = str(Path.home())
            disp_cwd = "~" + cwd[len(home):] if cwd.startswith(home) else cwd

            prompt_str = f"{Style.WITCH_PURPLE}🕯️  {Style.BOLD}spookshell{Style.RESET}:{Style.SPECTRAL_CYAN}{disp_cwd}{Style.RESET}{Style.PHANTOM_GREEN} ❯{Style.RESET} "
            user_input = input(prompt_str).strip()

            if not user_input:
                continue

            parts = shlex.split(user_input)
            cmd = parts[0].lower()

            # Built-in occult commands
            if cmd in ("exit", "quit", "q"):
                typewriter("The candles flicker and extinguish. The veil closes... until next year.", 0.02, Style.WITCH_PURPLE)
                break
            elif cmd in ("help", "?"):
                print_help()
            elif cmd in ("clear", "cls"):
                os.system("clear" if os.name != "nt" else "cls")
                print(BANNER)
            elif cmd == "haunt":
                cmd_haunt(ai)
            elif cmd == "seance":
                cmd_seance(ai, parts[1:])
            elif cmd == "ofrenda":
                if len(parts) > 2 and parts[1].lower() == "offer":
                    item = " ".join(parts[2:])
                    custom_offerings.append(item)
                    print(f"\n{Style.MARIGOLD_ORANGE}🌼 You have placed an offering upon the altar:{Style.RESET} {Style.BOLD}{item}{Style.RESET}")
                    print(f"{Style.DIM}The marigolds glow warmly with appreciation.{Style.RESET}\n")
                else:
                    cmd_ofrenda(custom_offerings)
            elif cmd == "exorcise":
                cmd_exorcise()
            elif cmd == "whisper":
                whisper = ai._offline_spectral_whisper("whisper", 0, "")
                print(f"\n{Style.WITCH_PURPLE}👻 [Phantom Whisper]{Style.RESET} {Style.ITALIC}{Style.SPECTRAL_CYAN}{whisper}{Style.RESET}\n")
            elif cmd == "web":
                web_file = SCRIPT_DIR / "web_ofrenda.html"
                if web_file.exists():
                    print(f"\n{Style.SPECTRAL_CYAN}🕸️  Opening the Web Ofrenda & Séance in your browser:{Style.RESET}")
                    print(f"   {Style.BOLD}file://{web_file}{Style.RESET}\n")
                    subprocess.run(["xdg-open", str(web_file)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                else:
                    print(f"{Style.BLOOD_RED}web_ofrenda.html not found.{Style.RESET}")
            elif cmd == "cd":
                # Handle cd inside the REPL
                target = parts[1] if len(parts) > 1 else str(Path.home())
                try:
                    os.chdir(os.path.expanduser(target))
                except Exception as e:
                    print(f"{Style.BLOOD_RED}cd: {e}{Style.RESET}")
            else:
                # Intercept and run real shell command
                execute_shell_command(user_input, ai)

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{Style.WITCH_PURPLE}The spirit connection severed. Fare thee well, mortal.{Style.RESET}")
            break

# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) > 1:
        # One-off command mode: spookshell <cmd>
        ai = SpectralAIEngine()
        subcmd = sys.argv[1]
        if subcmd == "seance":
            cmd_seance(ai, sys.argv[2:])
        elif subcmd == "ofrenda":
            cmd_ofrenda([])
        elif subcmd == "haunt":
            cmd_haunt(ai)
        elif subcmd == "exorcise":
            cmd_exorcise()
        elif subcmd in ("help", "--help", "-h"):
            print(BANNER)
            print_help()
        else:
            # Execute command wrapped in ghost mode
            cmd_str = " ".join(sys.argv[1:])
            execute_shell_command(cmd_str, ai)
    else:
        run_interactive_shell()

if __name__ == "__main__":
    main()
