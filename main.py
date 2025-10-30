import sys
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from metro_oop import load_data, Ticket, save_ticket, BASE_FARE, TICKETS_FILE
from metro_graph import MetroGraph

class MetroSystem:
   
    def __init__(self):
        print("Loading Metro System Data...")
        self.stations, self.lines, self.tickets_df = load_data()
        if not self.stations or not self.lines:
            sys.exit("Failed")
        
        self.graph = MetroGraph(self.stations, self.lines)
        print("Ready")

    def show_all_stations(self):
        
        print("\n--- Available Metro Stations ---")
        station_names = sorted(self.stations.keys())
        for i, name in enumerate(station_names, 1):
            lines = " | ".join(self.stations[name].lines)
            print(f"{i}. {name} (Lines: {lines})")
        print("--------------------------------")

    def find_connecting_line(self, station_a, station_b):
        
        lines_a = set(self.stations[station_a].lines)
        lines_b = set(self.stations[station_b].lines)
        common_lines = lines_a.intersection(lines_b)
        
    
        return common_lines.pop() if common_lines else None

    def generate_instructions(self, path):
       
        instructions = []
        current_line_name = None
        
        for i in range(len(path) - 1):
            current_station = path[i]
            next_station = path[i+1]
            
            connecting_line = self.find_connecting_line(current_station, next_station)
            
            if connecting_line and connecting_line != current_line_name:
                if not current_line_name:
                    
                    instructions.append(f"1. Start on **{connecting_line}** from **{current_station}**.")
                else:
                   
                    instructions.append(f"{len(instructions) + 1}. Change to **{connecting_line}** at **{current_station}**.")
                
                current_line_name = connecting_line
        
        if not instructions:
             return f"1. Travel directly from **{path[0]}** to **{path[-1]}**."
            
        
        instructions.append(f"{len(instructions) + 1}. Arrive at final destination **{path[-1]}**.")

        return "\n".join(instructions)

    def purchase_ticket(self):
        
        self.show_all_stations()
        
        start = input("\nEnter Start Station Name: ").strip()
        end = input("Enter End Station Name: ").strip()

        if start not in self.stations or end not in self.stations:
            print("\nInvalid station name. Please check the list and try again.")
            return

        if start == end:
            print("\nStart and End stations are the same. Price is Rs0.")
            return

       
        path = self.graph.get_shortest_path(start, end)

        if not path:
            print(f"\nNo route found between {start} and {end}.")
            return

        num_stops = len(path) - 1
        price = num_stops * BASE_FARE
        instructions = self.generate_instructions(path)
        
        new_ticket = Ticket(start, end, price, path, instructions)
        save_ticket(new_ticket)

        print(f"\n--- TICKET PURCHASED (ID: {new_ticket.ticket_id[:8]}...) ---")
        print(f"**Route:** {start} -> {end}")
        print(f"**Stops:** {num_stops}")
        print(f"**Price:** Rs {price}")
        print("\n**Travel Instructions:**")
        print(instructions.replace('**', '')) 
        print("-------------------------------------------------")


    def show_purchased_tickets(self):
      
        try:
          
            tickets_df = pd.read_csv(TICKETS_FILE)
            
            if tickets_df.empty:
                print("\n No tickets purchased yet.")
                return

            print("\n--- PURCHASED TICKETS ---")
            for _, row in tickets_df.iterrows():
                
                print(f"ID: **{row['ticket_id'][:8]}...**")
                print(f"  Route: {row['start_station']} -> {row['end_station']}")
                
                
                try:
                    path_list = eval(row['path'])
                    stops = len(path_list) - 1
                except:
                    stops = "N/A" 
                    
                print(f"  Price: Rs{row['price']} | Stops: {stops}")
                print(f"  Instructions: {row['instructions'].replace('**', '')[:50]}...")
                print("-" * 30)
            print("-----------------------------")

        except pd.errors.EmptyDataError:
            print("\n No tickets purchased yet.")
        except FileNotFoundError:
             print("\n No tickets file found. Purchase a ticket first.")
        except Exception as e:
            print(f"Error loading tickets: {e}")

    def create_graphical_map(self):
       
        print("\n Generating Metro Map...")
        G = nx.Graph()
        
       
        for start_station, neighbors in self.graph.graph_dict.items():
            for end_station in neighbors:
                G.add_edge(start_station, end_station)

   
        plt.figure(figsize=(12, 8))
        
       
        pos = nx.spring_layout(G, k=0.3, iterations=50) 
        
        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='skyblue', alpha=0.9)
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray')
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        
        plt.title("Metro Network Map")
        plt.axis('off')
        plt.show()
        print("Map displayed!")


    def run_cli(self):
        
        while True:
            print("\n==============================================")
            print("         Metro Ticket Purchasing System         ")
            print("==============================================")
            print("1. See all Metro Stations")
            print("2. Purchase a Ticket")
            print("3. See Purchased Tickets")
            print("4. Create Graphical Map (Brownie Point)")
            print("5. Exit")
            print("----------------------------------------------")
            
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.show_all_stations()
            elif choice == '2':
                self.purchase_ticket()
            elif choice == '3':
                self.show_purchased_tickets()
            elif choice == '4':
                self.create_graphical_map()
            elif choice == '5':
                print("Thank you for using the Metro System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    app = MetroSystem()
    app.run_cli()