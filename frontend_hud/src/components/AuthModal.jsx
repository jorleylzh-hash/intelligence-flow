import React, { useState, useContext, useEffect } from 'react';
import { X, Mail, Lock, User, CheckCircle, ArrowRight, Loader2 } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

export default function AuthModal({ isOpen, onClose, initialMode = 'login' }) {
    const { login } = useContext(AuthContext);
    const [mode, setMode] = useState(initialMode === 'signup' ? 'signup_step1' : 'login');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    
    // FORM DATA
    const [formData, setFormData] = useState({
        email: '', password: '', full_name: '', code: ''
    });

    const API_URL = "http://localhost:8000";

    useEffect(() => {
        if (isOpen) {
            setMode(initialMode === 'signup' ? 'signup_step1' : 'login');
            setError('');
        }
    }, [isOpen, initialMode]);

    // Validação de Senha
    const passwordRequirements = [
        { id: 1, text: "Mínimo 8 caracteres", regex: /.{8,}/ },
        { id: 2, text: "Letra Maiúscula", regex: /[A-Z]/ },
        { id: 3, text: "Número", regex: /[0-9]/ },
        { id: 4, text: "Símbolo (!@#$)", regex: /[^A-Za-z0-9]/ },
    ];
    const isPasswordValid = passwordRequirements.every(req => req.regex.test(formData.password));

    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            // LOGIN
            if (mode === 'login') {
                const res = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email: formData.email, password: formData.password})
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || "Erro no login");
                login(data.user);
                onClose();
            }

            // PASSO 1: SÓ NOME E EMAIL (AQUI ESTÁ A MÁGICA)
            else if (mode === 'signup_step1') {
                const res = await fetch(`${API_URL}/auth/initiate-signup`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email: formData.email, full_name: formData.full_name})
                });
                
                if (!res.ok) {
                    const data = await res.json();
                    throw new Error(data.detail || "Erro ao iniciar cadastro");
                }
                setMode('signup_step2'); // Manda para tela de código
            }

            // PASSO 2: CÓDIGO
            else if (mode === 'signup_step2') {
                if (formData.code.length < 4) throw new Error("Código inválido");
                setMode('signup_step3'); // Manda para tela de senha
            }

            // PASSO 3: SENHA FINAL
            else if (mode === 'signup_step3') {
                if (!isPasswordValid) throw new Error("Senha fraca");
                const res = await fetch(`${API_URL}/auth/complete-signup`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        email: formData.email, code: formData.code, password: formData.password
                    })
                });
                if (!res.ok) {
                    const data = await res.json();
                    throw new Error(data.detail || "Erro ao finalizar");
                }
                login({email: formData.email, name: formData.full_name});
                onClose();
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm">
            <div className="relative w-full max-w-md bg-[#09090b] border border-slate-800 rounded-2xl shadow-2xl p-8">
                <button onClick={onClose} className="absolute top-4 right-4 text-slate-500 hover:text-white"><X size={20} /></button>
                
                <h2 className="text-xl font-bold text-white mb-6">
                    {mode === 'login' ? 'ACESSO AO SISTEMA' : 'NOVA CREDENCIAL'}
                </h2>

                {error && <div className="mb-4 p-3 bg-red-900/30 border border-red-500/30 text-red-400 text-sm rounded">{error}</div>}

                <form onSubmit={handleSubmit} className="space-y-4">
                    
                    {/* VISUALIZAÇÃO CONDICIONAL: SE FOR PASSO 1, MOSTRA SÓ EMAIL E NOME */}
                    {mode === 'signup_step1' && (
                        <div className="space-y-4 animate-fadeIn">
                            <div className="relative">
                                <User className="absolute left-3 top-3 text-slate-500" size={18} />
                                <input className="w-full bg-slate-950 border border-slate-800 rounded p-2.5 pl-10 text-white outline-none focus:border-cyan-500" 
                                    type="text" placeholder="Nome Completo" required value={formData.full_name} onChange={e => setFormData({...formData, full_name: e.target.value})} />
                            </div>
                            <div className="relative">
                                <Mail className="absolute left-3 top-3 text-slate-500" size={18} />
                                <input className="w-full bg-slate-950 border border-slate-800 rounded p-2.5 pl-10 text-white outline-none focus:border-cyan-500" 
                                    type="email" placeholder="E-mail Corporativo" required value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} />
                            </div>
                        </div>
                    )}

                    {/* SE FOR PASSO 2: CÓDIGO */}
                    {mode === 'signup_step2' && (
                        <div className="text-center space-y-4 animate-fadeIn">
                            <p className="text-sm text-slate-400">Código enviado para {formData.email}</p>
                            <input className="w-full bg-slate-950 border border-cyan-500/50 rounded p-3 text-center text-2xl tracking-[5px] text-cyan-400 font-mono outline-none focus:border-cyan-400" 
                                type="text" placeholder="CODIGO" required value={formData.code} onChange={e => setFormData({...formData, code: e.target.value})} />
                        </div>
                    )}

                    {/* SE FOR PASSO 3: SENHA */}
                    {mode === 'signup_step3' && (
                        <div className="space-y-4 animate-fadeIn">
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 text-slate-500" size={18} />
                                <input className="w-full bg-slate-950 border border-slate-800 rounded p-2.5 pl-10 text-white outline-none focus:border-cyan-500" 
                                    type="password" placeholder="Defina sua Senha" required value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} />
                            </div>
                            <div className="grid grid-cols-2 gap-2 mt-2">
                                {passwordRequirements.map(req => {
                                    const isValid = req.regex.test(formData.password);
                                    return (
                                        <div key={req.id} className={`text-[10px] flex items-center gap-1 transition-colors ${isValid ? 'text-emerald-400' : 'text-slate-600'}`}>
                                            {isValid ? <CheckCircle size={10} /> : <div className="w-2.5 h-2.5 rounded-full border border-slate-600"/>}
                                            {req.text}
                                        </div>
                                    )
                                })}
                            </div>
                        </div>
                    )}

                    {/* SE FOR LOGIN */}
                    {mode === 'login' && (
                         <div className="space-y-4 animate-fadeIn">
                            <div className="relative"><Mail className="absolute left-3 top-3 text-slate-500" size={18} /><input className="w-full bg-slate-950 border border-slate-800 rounded p-2.5 pl-10 text-white outline-none focus:border-cyan-500" type="email" placeholder="Email" required value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} /></div>
                            <div className="relative"><Lock className="absolute left-3 top-3 text-slate-500" size={18} /><input className="w-full bg-slate-950 border border-slate-800 rounded p-2.5 pl-10 text-white outline-none focus:border-cyan-500" type="password" placeholder="Senha" required value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} /></div>
                         </div>
                    )}

                    <button type="submit" disabled={loading} className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 rounded flex justify-center items-center gap-2 transition-all shadow-[0_0_15px_rgba(6,182,212,0.3)]">
                        {loading ? <Loader2 className="animate-spin" /> : (
                            <>
                                {mode === 'login' && 'ENTRAR'}
                                {mode === 'signup_step1' && 'ENVIAR CÓDIGO'}
                                {mode === 'signup_step2' && 'VALIDAR'}
                                {mode === 'signup_step3' && 'CRIAR CONTA'}
                                {!['login', 'signup_step3'].includes(mode) && <ArrowRight size={16} />}
                            </>
                        )}
                    </button>

                    <div className="text-center text-xs text-slate-500 mt-4">
                        {mode === 'login' ? 
                            <span className="cursor-pointer hover:text-cyan-400" onClick={() => setMode('signup_step1')}>Criar nova conta</span> : 
                            <span className="cursor-pointer hover:text-cyan-400" onClick={() => setMode('login')}>Voltar para Login</span>
                        }
                    </div>
                </form>
            </div>
        </div>
    );
}