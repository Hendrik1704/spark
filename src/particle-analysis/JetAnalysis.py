import numpy as np
import fastjet as fj
import csv
from Particle import Particle

class JetAnalysis:
    """
    This class analyzes events for different ptHat bins using the fastjet
    python package.
    """
    def __init__(self,hadron_data,jet_R,jet_eta_cut,jet_pt_min,pt_hat_max,\
                 jet_algorithm=fj.antikt_algorithm):
        self.hadron_data_ = hadron_data
        self.jet_R_ = jet_R
        self.jet_eta_cut_ = jet_eta_cut
        self.jet_pt_min_ = jet_pt_min
        self.pt_hat_max_ = pt_hat_max
        self.jet_algorithm_ = jet_algorithm

    def create_fastjet_PseudoJets(self,event_hadrons):
        event_list_PseudoJets = []
        for hadron in range(len(event_hadrons)):
            pseudo_jet = fj.PseudoJet(event_hadrons[hadron].px,\
                                     event_hadrons[hadron].py,\
                                        event_hadrons[hadron].pz,\
                                            event_hadrons[hadron].E)
            event_list_PseudoJets.append(pseudo_jet)
        return event_list_PseudoJets

    def fill_associated_particles(self,jet,event):
        # select particles in jet cone
        associated_hadrons = []
        for hadron in self.hadron_data_[event]:
            fastjet_particle = fj.PseudoJet(hadron.px,hadron.py,\
                                            hadron.pz,hadron.E)
            delta_eta = fastjet_particle.eta() - jet.eta()
            delta_phi = fastjet_particle.delta_phi_to(jet)
            delta_r = np.sqrt(delta_eta**2. + delta_phi**2.)

            if delta_r < self.jet_R_:
                associated_hadrons.append(hadron)
        return associated_hadrons

    def write_jet_output(self,output_filename,jet,associated_hadrons,new_file=False):
        # jet data from reconstruction
        jet_status = 10
        jet_pid = 10
        output_list = []
        if jet.perp() < self.pt_hat_max_:
            output_list = [[0,jet.perp(),jet.eta(),jet.phi(),jet_status,\
                            jet_pid,jet.e()]]

            # associated hadrons
            for i, associated in enumerate(associated_hadrons):
                pseudo_jet = fj.PseudoJet(associated.px,associated.py,\
                                          associated.pz,associated.E)
                output = [i+1,pseudo_jet.perp(),pseudo_jet.eta(),\
                          pseudo_jet.phi(),associated.status,\
                            associated.pdg,associated.E]
                output_list.append(output)

        mode = 'a'
        if new_file == True:
            mode = 'w'
        f = open(output_filename,mode,newline='')
        writer = csv.writer(f)
        writer.writerows(output_list)
        f.close()
        return False

    def perform_jet_analysis(self,output_filename):
        """
        Perform the jet analysis for multiple events. The function generates a
        file containing the jets consisting of a leading particle and associated
        hadrons in the jet cone.

        Parameters
        ----------
        output_filename: string
            Filename for the jet output.
        """
        for event in range(len(self.hadron_data_)):
            new_file = False
            all_hadrons_event = self.hadron_data_[event]
            event_FastJet = self.create_fastjet_PseudoJets(all_hadrons_event)

            jet_definition = fj.JetDefinition(self.jet_algorithm_, self.jet_R_)
            jet_selector = fj.SelectorAbsEtaMax(self.jet_eta_cut_)

            if event == 0:
                print("jet definition is:", jet_definition)
                print("jet selector is:", jet_selector)
                # create a new file for the first event in the dataset
                new_file = True

            # perform the jet finiding algorithm
            cluster = fj.ClusterSequence(event_FastJet, jet_definition)
            jets = fj.sorted_by_pt(cluster.inclusive_jets(self.jet_pt_min_))
            jets = jet_selector(jets)

            # get the associated particles in the jet cone
            for jet in jets:
                associated_particles = self.fill_associated_particles(jet, event)
                new_file = self.write_jet_output(output_filename,jet,\
                                            associated_particles,new_file)
