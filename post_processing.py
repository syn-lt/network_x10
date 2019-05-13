
import pickle
import numpy as np

from brian2.units import ms,mV,second,Hz

from analysis.methods.process_survival import extract_survival
from analysis.methods.process_turnover_pd import extract_lifetimes

from analysis.srvprb_all import srvprb_all_figure
from analysis.srvprb_EE import srvprb_EE_figure
from analysis.srvprb_EI import srvprb_EI_figure


def post_process_turnover(tr, connections='EE'):

    if connections=='EE':
        cn=''
    elif connections=='EI':
        cn='_EI'

    t_cut = tr.pp_tcut
    t_split = (tr.T2-t_cut)/2.

    if t_split/second > 0:

        # E<-E connections

        with open('builds/%.4d/raw/turnover%s.p' %(tr.v_idx,cn), 'rb') as pfile:
            turnover = pickle.load(pfile)

        # tr.N_e only used for s_id creation,
        # and since tr.N_i > tr.N_e,
        # tr.NE is correct for both 'EE' & 'EI'
        full_t, ex_ids = extract_survival(turnover,
                                          tr.N_e,
                                          t_split=t_split,
                                          t_cut=t_cut)

        fpath = 'builds/%.4d/raw/survival%s_full_t.p' %(tr.v_idx, cn)
        with open(fpath, 'wb') as pfile:
            out = {'t_split': t_split, 't_cut': t_cut,
                   'full_t': full_t, 'excluded_ids': ex_ids}
            pickle.dump(out, pfile)



    Tmax = tr.sim.T1+tr.sim.T2+tr.sim.T3

    lts_wthsrv, lts_dthonly, ex_ids = extract_lifetimes(turnover,
                                                        tr.N_e,
                                                        t_cut=t_cut,
                                                        Tmax=Tmax)

    bpath = 'builds/%.4d' %(tr.v_idx)
    for bin_w in [0.1*second, 0.5*second, 1*second, 10*second, 100*second]:

        bins = np.arange(bin_w/second,
                         Tmax/second+2*bin_w/second,
                         bin_w/second)

        f_add = 'bin%dcs' %(int(bin_w/second*10.))

        counts, edges = np.histogram(lts_wthsrv, bins=bins,
                                     density=True)
        centers = (edges[:-1] + edges[1:])/2.            
        
        with open(bpath+'/raw/lts%s_wthsrv_' %cn +f_add+'.p', 'wb') as pfile:
            out = {'Tmax': Tmax, 't_cut': t_cut,
                   'counts': counts, 'excluded_ids': ex_ids,
                   'bins': bins, 'centers': centers, 'bin_w': bin_w}
            pickle.dump(out, pfile)


        counts, edges = np.histogram(lts_dthonly, bins=bins,
                                     density=True)
        centers = (edges[:-1] + edges[1:])/2.            

        with open(bpath+'/raw/lts%s_dthonly_' %cn +f_add+'.p', 'wb') as pfile:
            out = {'Tmax': Tmax, 't_cut': t_cut,
                   'counts': counts, 'excluded_ids': ex_ids,
                   'bins': bins, 'centers': centers, 'bin_w': bin_w}
            pickle.dump(out, pfile)


    for nbins in [25,50,100,250,500,1000,2500,5000]:

        bins = np.logspace(np.log10(1),
                           np.log10((Tmax-t_cut)/second+0.5),
                           num=nbins)

        f_add = 'lognbin%d' %(nbins)

        counts, edges = np.histogram(lts_wthsrv, bins=bins,
                                     density=True)
        centers = (edges[:-1] + edges[1:])/2.            

        with open(bpath+'/raw/lts%s_wthsrv_' %cn +f_add+'.p', 'wb') as pfile:
            out = {'Tmax': Tmax, 't_cut': t_cut,
                   'counts': counts, 'excluded_ids': ex_ids,
                   'bins': bins, 'centers': centers, 'nbins': nbins}
            pickle.dump(out, pfile)


        counts, edges = np.histogram(lts_dthonly, bins=bins,
                                     density=True)
        centers = (edges[:-1] + edges[1:])/2.            

        with open(bpath+'/raw/lts%s_dthonly_' %cn +f_add+'.p', 'wb') as pfile:
            out = {'Tmax': Tmax, 't_cut': t_cut,
                   'counts': counts, 'excluded_ids': ex_ids,
                   'bins': bins, 'centers': centers, 'nbins': nbins}
            pickle.dump(out, pfile)




def post_process(tr):

    post_process_turnover(tr, 'EE')
    post_process_turnover(tr, 'EI')

    srvprb_EE_figure('builds/%.4d'%(tr.v_idx))
    srvprb_EI_figure('builds/%.4d'%(tr.v_idx))
    srvprb_all_figure('builds/%.4d'%(tr.v_idx))





        
