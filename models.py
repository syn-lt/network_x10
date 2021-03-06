
condlif_poisson = '''
              dV/dt = (El-V + (gfwd+ge)*(Ee-V) + gi*(Ei-V))/tau : volt
              Vt : volt 
              dge /dt = -ge/tau_e : 1
              dgfwd /dt = -gfwd/tau_e : 1
              dgi /dt = -gi/tau_i : 1

              Asum : 1
              '''


condlif_memnoise = '''
              dV/dt = (El-V + ge*(Ee-V) + gi*(Ei-V))/tau +  mu/tau + (sigma * xi) / (tau **.5) : volt
              Vt : volt 
              dge /dt = -ge/tau_e : 1
              dgi /dt = -gi/tau_i : 1

              Asum : 1

              sigma: volt (constant)
              mu : volt (constant)
              '''


# refractory period???

nrnEE_thrshld = 'V > Vt'

nrnEE_reset = 'V = Vr_e'

poisson_mod = 'PInp_a : 1'

# !--- add event-driven for efficiency ---!
# dApre  /dt = -Apre/taupre  : 1 (event-driven)
# dApost /dt = -Apost/taupost : 1 (event-driven)

synEE_static = 'a : 1'
synEE_noise  = '''da/dt = syn_active*syn_sigma**0.5*xi : 1
                  syn_sigma : 1/second (shared)'''

synEE_mod = '''            
            syn_active : integer

            dApre  /dt = -Apre/taupre  : 1 (event-driven)
            dApost /dt = -Apost/taupost : 1 (event-driven)

            Asum_post = a : 1 (summed)         
            insert_P : 1 (shared) 
            p_inactivate : 1 (shared)
            stdp_active : integer (shared)

            scl_rec_start : second (shared)
            scl_rec_max   : second (shared)

            stdp_rec_start : second (shared)
            stdp_rec_max   : second (shared)

            ATotalMax : 1
            '''



synEE_p_activate = '''
                   r = rand()
                   syn_active = int(r < p_ee)
                   a = syn_active*a
                   '''

synEE_pre = '''
            ge_post += syn_active*a
            Apre = syn_active*Aplus
            '''

synEE_pre_STDP = '''
                 a = syn_active*clip(a+Apost*stdp_active, 0, amax)
                 '''

synEE_pre_rec = '''
                dummy = record_spk(t, i, j, a, Apre, Apost, syn_active, 0, stdp_rec_start, stdp_rec_max)
                '''

synEE_post = '''
             Apost = syn_active*Aminus
             '''

synEE_post_STDP = '''
                  a = syn_active*clip(a+Apre*stdp_active, 0, amax)
                  '''

synEE_post_rec = '''
                 dummy = record_spk(t, i, j, a, Apre, Apost, syn_active, 1, stdp_rec_start, stdp_rec_max)
                 '''

# synEE_scaling = '''
#                 a = clip(a*(ATotalMax/Asum_post),0,amax)
#                 '''
synEE_scaling = '''
                a = syn_active*syn_scale(a, ATotalMax, Asum_post, eta_scaling, t, syn_active, scl_rec_start, scl_rec_max, i, j)
                '''


# rand() == uniform(0,1)
#strct_mod = ''

strct_mod_thrs = '''
                 r = rand()
                 should_stay_active = int(a > prn_thrshld)
                 should_become_active = int(r < insert_P)
                 was_active_before = syn_active
                 syn_active = int(syn_active==1) * int(should_stay_active) \
                    + int(syn_active==0) * int(should_become_active)
                 a = a*int(was_active_before==1)*int(syn_active==1) \
                    + a_insert*int(was_active_before==0)*int(syn_active==1)
                 '''

turnover_rec_mod = '''
                   dummy = record_turnover(t, was_active_before, should_become_active, should_stay_active, syn_active, i, j)
                   '''
 

strct_mod = '''
            r = rand()
            should_stay_active = int(a > strct_c) + int(a<= strct_c)*int(r>p_inactivate)
            s = rand()
            should_become_active = int(s < insert_P)
            was_active_before = syn_active
            syn_active = int(syn_active==1) * int(should_stay_active) \
                     + int(syn_active==0) * int(should_become_active)
            a = a*int(was_active_before==1)*int(syn_active==1) \
                + a_insert*int(was_active_before==0)*int(syn_active==1)
            '''
