import random

class Process:
    def __init__(self, pid, priority, exec_time, resources):
        self.pid = pid
        self.priority = priority
        self.exec_time = exec_time
        self.resources = resources
        self.needs = []
        self.alive = True
        self.preempt_count = 0
        self.checkpoint = exec_time * 0.5
    
    def __str__(self):
        return f"P{self.pid}"

class Deadlock:
    def __init__(self):
        self.procs = []
        self.avail = []
        
    def setup(self):
        print("=" * 50)
        print("DEADLOCK SCENARIO")
        print("=" * 50)
        
        p1 = Process(1, 3, 70, [1])
        p1.needs = [2]
        
        p2 = Process(2, 2, 50, [2])
        p2.needs = [3]
        
        p3 = Process(3, 1, 30, [3])
        p3.needs = [1]
        
        p4 = Process(4, 4, 90, [4])
        p4.needs = [2]
        
        self.procs = [p1, p2, p3, p4]
        self.avail = [5]
        
        print("\nProcesses:")
        for p in self.procs:
            print(f"  {p}: has R{p.resources}, needs R{p.needs}")
        print(f"\nFree: R{self.avail}")
        print("\nDEADLOCK: P1->P2->P3->P1 cycle!")
        
    def is_deadlock(self):
        waiting = [p for p in self.procs if p.alive and p.needs]
        return len(waiting) >= 3
    
    # Method 1: Kill all
    def kill_all(self):
        print("\n" + "=" * 50)
        print("TERMINATE ALL")
        print("=" * 50)
        
        dead = [p for p in self.procs if p.alive]
        
        print(f"\nKilling {len(dead)} processes...")
        
        freed = []
        lost = 0
        
        for p in dead:
            print(f"\nX Killing {p}")
            print(f"  Lost: {p.exec_time}%")
            print(f"  Freed: R{p.resources}")
            
            freed.extend(p.resources)
            lost += p.exec_time
            p.alive = False
            p.resources = []
        
        self.avail.extend(freed)
        
        print(f"\nDone! Lost: {lost}%")
        print(f"Free now: R{sorted(self.avail)}")
        print(f"\nPros: Fast")
        print(f"Cons: Wasteful")
    
    # Method 2: Kill one by one
    def kill_one(self):
        print("\n" + "=" * 50)
        print("TERMINATE ONE AT A TIME")
        print("=" * 50)
        
        i = 1
        
        while self.is_deadlock():
            print(f"\n--- Round {i} ---")
            
            victim = self.pick_victim()
            
            print(f"\nKilling {victim}")
            print(f"  Why: Low priority, least done")
            print(f"  Lost: {victim.exec_time}%")
            
            self.avail.extend(victim.resources)
            victim.alive = False
            victim.resources = []
            
            print(f"  Free: R{sorted(self.avail)}")
            
            if not self.is_deadlock():
                print(f"\nFixed in {i} kills!")
                break
            else:
                print(f"  Still deadlocked...")
            
            i += 1
        
        print(f"\nPros: Saves work")
        print(f"Cons: Slower")
    
    def pick_victim(self):
        alive = [p for p in self.procs if p.alive]
        
        def cost(p):
            return p.priority * 100 + p.exec_time * 50 - len(p.resources) * 20
        
        return min(alive, key=cost)
    
    # Method 3: Preempt resources
    def preempt(self):
        print("\n" + "=" * 50)
        print("RESOURCE PREEMPTION")
        print("=" * 50)
        
        print("\nPicking victim...")
        
        victim = self.pick_preempt_victim()
        
        print(f"\nVictim: {victim}")
        print(f"  Priority: {victim.priority}")
        print(f"  Done: {victim.exec_time}%")
        print(f"  Has: R{victim.resources}")
        print(f"  Preempted before: {victim.preempt_count}x")
        
        # Rollback
        old_time = victim.exec_time
        safe = victim.checkpoint
        
        print(f"\nRolling back {victim}...")
        print(f"  From: {old_time}%")
        print(f"  To: {safe}%")
        
        # Take resources
        take = victim.resources[:-1]
        victim.resources = victim.resources[-1:]
        self.avail.extend(take)
        
        print(f"  Took: R{take}")
        print(f"  Left: R{victim.resources}")
        print(f"  Free: R{sorted(self.avail)}")
        
        victim.exec_time = safe
        victim.preempt_count += 1
        
        print(f"\nDone! {victim} at {safe}%")
        
        if victim.preempt_count >= 3:
            print(f"\nWARNING: {victim} starving! ({victim.preempt_count}x)")
        
        print(f"\nPros: Less loss")
        print(f"Cons: Complex")
    
    def pick_preempt_victim(self):
        alive = [p for p in self.procs if p.alive]
        
        def cost(p):
            return (p.priority * 100 + 
                    p.exec_time * 50 - 
                    len(p.resources) * 30 + 
                    p.preempt_count * 80)
        
        return min(alive, key=cost)


# Run demos
def run():
    print("DEADLOCK RECOVERY DEMO\n")
    
    # Demo 1
    print("\n>>> DEMO 1: KILL ALL")
    d1 = Deadlock()
    d1.setup()
    d1.kill_all()
    
    # Demo 2
    print("\n\n>>> DEMO 2: KILL ONE BY ONE")
    d2 = Deadlock()
    d2.setup()
    d2.kill_one()
    
    # Demo 3
    print("\n\n>>> DEMO 3: PREEMPTION")
    d3 = Deadlock()
    d3.setup()
    d3.preempt()
    
    print("\n" + "=" * 50)
    print("COMPARISON")
    print("=" * 50)
    print("\nKILL ALL:")
    print("  + Fast, simple")
    print("  - Loses everything")
    
    print("\nKILL ONE:")
    print("  + Saves some work")
    print("  - Takes time")
    
    print("\nPREEMPT:")
    print("  + Minimal loss")
    print("  - Needs checkpoints")
    print("  - Can starve process")

if __name__ == "__main__":
    run()
